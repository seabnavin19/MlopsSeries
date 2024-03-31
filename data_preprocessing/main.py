from prefect import flow, task

@task
def say_hello():
    print("Hello, world!")

@task
def say_name(name):
    print(f"my name is, {name}!")

@flow
def greeting(name):
    say_hello()
    say_name(name)
    

if __name__ == "__main__":
    greeting(name="Navin")