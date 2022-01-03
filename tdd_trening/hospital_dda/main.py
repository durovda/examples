from tdd_trening.hospital_dda.application import Application
from tdd_trening.hospital_dda.console import Console
from tdd_trening.hospital_dda.hospital import Hospital

if __name__ == "__main__":
    hospital = Hospital([1 for x in range(200)])
    console = Console()
    app = Application(hospital=hospital,
                      input_stream=console,
                      output_stream=console)
    app.main()
