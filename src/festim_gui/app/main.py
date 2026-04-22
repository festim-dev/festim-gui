from .core import FestimGUI


def main(server=None, **kwargs):
    app = FestimGUI(server)
    app.server.start(**kwargs)


if __name__ == "__main__":
    main()
