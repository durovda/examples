from tdd_trening.hospital_dda.console import Console

if __name__ == "__main__":
    input_stream = Console()
    message = input_stream.get_message('Введите ID пациента: ')
    print(message)

    output_stream = Console()
    output_stream.send_message('Статус пациента: "Болен"')