from src.my_project.subscriber import Subscriber

if __name__ == "__main__":
    sub = Subscriber()
    sub.subscribe("log-channel")
