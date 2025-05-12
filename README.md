# rpl-etec

django re-purposed version of rpl2.0

# Try it
Available at
[www.rpletec.fun](www.rpletec.fun)

# Notes

## Concurrent Code Submission Handler

```mermaid
sequenceDiagram
    participant User1
    participant User2
    participant WebProcess1
    participant WebProcess2
    participant FileSystem
    participant TestService

    rect rgb(220, 240, 220)
        Note over User1, TestService: Improved Implementation
        User1 ->> WebProcess1: Submit Code A
        User2 ->> WebProcess2: Submit Code B

        par Process A
            WebProcess1 ->> FileSystem: Create unique temp dir for A with atomic
            WebProcess1 ->> TestService: Run tests for A in isolation
        and Process B
            WebProcess2 ->> FileSystem: Create unique temp dir for B with atomic
            WebProcess2 ->> TestService: Run tests for B in isolation
        end
    end
```

        submissions: ManyToManyField(CodeSubmission)
## User

Default `username` is `NAME[0]`+`SURNAME[1:]`:

* `pflores` is `Pablo Flores`

```mermaid
classDiagram
    class User {
        id: BigAutoField
        username: CharField
        email: EmailField
        first_name: CharField
        last_name: CharField
        is_staff: BooleanField
        is_active: BooleanField
        date_joined: DateTimeField
    }
    class UserProfile {
        user_id: ForeignKey(User)
    }
    UserProfile --|> User
    User o-- Group
```

## Group

`Group` is a Django model that allows to group users and define permissions for them. For example, a `Teacher` group can
have permissions to **create** Units and Excercices , while a `Student` group can only have permissions to view
their courses and submit code.

### Student Group

`Permissions:

* Can view their courses
* Can view the course's units
* Can view the unit's excercises
* Can submit code for excercises
* Can view othe Student's Actions

### Teacher Group

Permissions:

* Can view their courses (admin-assigned)
* Can create and edit Units
* Can create and edit Excercises
* Can delete Units and Excercises
* Can view all Student's Actions
* Can add and remove students from their courses

`


## Code Submissions

```mermaid
classDiagram
    class CodeSubmission {
        id: BigAutoField
        student: ForeignKey(User)
        excercise: ForeignKey(Excercise)
        code: TextField
        created: DateTimeField
        succes: BooleanField
        result: TextField
    }
```


## Course and Unit

```mermaid
classDiagram
    class Course {
        id: BigAutoField
        title: CharField
        slug: SlugField
        group: ChoiceField
    }

    class Unit {
        id: BigAutoField
        course: ForeignKey(Course)
        title: CharField
        slug: SlugField
        description: TextField
    }

    class Excercise {
        title: CharField
        slug: SlugField
        statement: TextField
        initial_code: TextField
        test: TextField
        solution: TextField
        function_name: CharField
        libraries: ChoiceField
        
        files: ManyToManyRel(Files)
        unit: ForeignKey(Unit)
        
    }

    Course "1" *-- "*" Unit
    Unit "1" *-- "*" Excercise
```

## Excercise

```mermaid
classDiagram
    class Excercise {
        id: BigAutoField
        title: CharField
        statement: TextField
        test: TextField
        solution: TextField
        
        unit: ForeignKey(Unit)
        
    }

```

## Files

```mermaid

classDiagram
    class File {
        id: BigAutoField
        name: CharField
        content: TextField
    }

```

## Actions

Record actions taken by users `USER` `VERB` `ACTIVITY` at `TIME`:

* `pflores` has completed `excercise 1` at `10:00`.
* `pflores` has completed `Unit 1` at `13:00`.

### Implementation

An `Action` is created every time a student completes a unit or excercise with `success` in all tests.

```python
class Action(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='actions', on_delete=models.CASCADE)
    verb = models.CharField(max_length=255)
    created = models.DatTimeField(auto_now_add=True)
    target_ct = models.ForeignKey(
        ContentType,
        blank=True,
        null=True,
        related_name='target_obj',
        on_delete=models.CASCADE
    )
    target_id = models.PositiveIntegerField(blank=True, null=True)
    target = GenericForeignKey('target_ct', 'target_id')
```

* `taget_ct`: A FK field that points to the ContentType model
* `target_id`: An integer field that points to the target object id (the `ACTIVITY` should have integer pk's)
* `target`: A GenericForeignKey field to the related object based on the combination of the two previous fields

### Model diagram

```mermaid
classDiagram
    direction LR
    class ContentType {
        id: BigAutoField
        app_label: CharField
        model: CharField
    }

    class Action {
        id: BigAutoField
        user: ForeignKey
        verb: ForeignKey
        target_ct: ForeignKey
        target_id: IntegerField
    }

    Action "*" <..> "1" ContentType
```

## Celery

### Configuration

We use *redis* as a message brocker and end point for celery. The idea is to have a single worker responsible for the
execution of any type of test involving code submissions (students) or excercise creation (teachers).

### Tasks

#### `test_code`

The `test_code` functional task is responsible for executing the `run_test` function from the `CodeTestingService`.

The task takes in the id of the CodeSubmission object by the user. This `submission_id` is used to retrieve the code,
then the code is tested using the `run_test` that checks _several system security checks_ beside testing the code with
the corresponding set of unittest cases assigned to the `Excercise`.

## Testing service

The `CodeTestingService` is a class that is responsible for retrieving the `Excercise` corresponding to the
`submission_id` generated by the code submission. Then, it gets the test cases from the `Excercise` and runs them to
test the submitted code. In the proccess, the service creates a temporary directory to store the code and the test
cases, checks the code for security issues, runs the test cases and deletes the temporary files.

## CodeSubmission

