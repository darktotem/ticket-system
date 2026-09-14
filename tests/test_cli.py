from main import TicketApp


def test_app_initializes_with_no_logged_in_user(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    app = TicketApp()
    assert app.current_user is None


def test_role_restricted_menu_blocks_guest(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    app = TicketApp()
    app.show_employee_menu()  # current_user is None
    captured = capsys.readouterr()
    assert "Please login first." in captured.out