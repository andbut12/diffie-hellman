from gui import GUIInterface


def main():
    interface = GUIInterface(
        size="600x560",
        title="Калькулятор ключей для протокола Диффи-Хеллмана"
    )

    interface.run()


if __name__ == "__main__":
    main()
