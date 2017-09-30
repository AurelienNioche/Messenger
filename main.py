def main():
    from utils.config_management import ConfigFilesManager

    ConfigFilesManager.run()

    from messenger import model

    m = model.Model()
    m.run()


if __name__ == "__main__":
    main()
