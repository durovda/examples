from tdd_trening.hospital_dda.console import Console

if __name__ == "__main__":
    input_stream = Console()
    message = input_stream.input('Введите ID пациента: ')
    print(message)

    output_stream = Console()
    output_stream.print('Статус пациента: "Болен"')
