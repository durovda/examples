from tdd_trening.hospital_dda.application import Application
from tdd_trening.hospital_dda.commands import Commands
from tdd_trening.hospital_dda.console import Console
from tdd_trening.hospital_dda.dialog_with_user import DialogWithUser
from tdd_trening.hospital_dda.hospital import Hospital

if __name__ == "__main__":
    hospital = Hospital([1 for x in range(200)])
    console = Console()
    dialog_with_user = DialogWithUser(console)
    commands = Commands(hospital, dialog_with_user)
    app = Application(dialog_with_user, commands)

    app.main()
