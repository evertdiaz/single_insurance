import pytest
from algokit_utils import (
    ApplicationClient,
    ApplicationSpecification,
    get_localnet_default_account,
)
from algosdk.v2client.algod import AlgodClient

from smart_contracts.insurance import contract as insurance_contract


@pytest.fixture(scope="session")
def insurance_app_spec(algod_client: AlgodClient) -> ApplicationSpecification:
    return insurance_contract.app.build(algod_client)


@pytest.fixture(scope="session")
def insurance_client(
    algod_client: AlgodClient, insurance_app_spec: ApplicationSpecification
) -> ApplicationClient:
    client = ApplicationClient(
        algod_client,
        app_spec=insurance_app_spec,
        signer=get_localnet_default_account(algod_client),
        template_values={"UPDATABLE": 1, "DELETABLE": 1},
    )
    client.create()
    return client


def test_says_hello(insurance_client: ApplicationClient) -> None:
    result = insurance_client.call(insurance_contract.hello, name="World")

    assert result.return_value == "Hello, World"
