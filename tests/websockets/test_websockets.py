from uuid import uuid4

from fastapi.testclient import TestClient

from app.core.websocket_manager import manager
from app.main import app


def test_websocket_connection():
    company_id = uuid4()

    with TestClient(app) as client:
        with client.websocket_connect(
            f'/ws/companies/{company_id}'
        ):
            assert company_id in manager.connections
            assert len(manager.connections[company_id]) == 1


def test_websocket_disconnect():
    company_id = uuid4()

    with TestClient(app) as client:
        with client.websocket_connect(
            f'/ws/companies/{company_id}'
        ):
            assert company_id in manager.connections

        assert company_id not in manager.connections


def test_multiple_websocket_connections():
    company_id = uuid4()

    with TestClient(app) as client:
        with client.websocket_connect(
            f'/ws/companies/{company_id}'
        ):
            assert len(manager.connections[company_id]) == 1

            with client.websocket_connect(
                f'/ws/companies/{company_id}'
            ):
                assert len(manager.connections[company_id]) == 2

            assert len(manager.connections[company_id]) == 1

        assert company_id not in manager.connections


def test_websocket_connections_are_separated_by_company():
    company_1 = uuid4()
    company_2 = uuid4()

    with TestClient(app) as client:
        with client.websocket_connect(
            f'/ws/companies/{company_1}'
        ):
            with client.websocket_connect(
                f'/ws/companies/{company_2}'
            ):
                assert company_1 in manager.connections
                assert company_2 in manager.connections

                assert len(manager.connections[company_1]) == 1
                assert len(manager.connections[company_2]) == 1

        assert company_1 not in manager.connections
        assert company_2 not in manager.connections
