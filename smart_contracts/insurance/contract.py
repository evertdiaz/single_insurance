import beaker
import pyteal as pt

class myState :
    assetName = beaker.GlobalStateValue(stack_type=pt.TealType.bytes)
    assetDesc = beaker.GlobalStateValue(stack_type=pt.TealType.bytes)
    assetVal= beaker.GlobalStateValue(stack_type=pt.TealType.uint64)
    asaID = beaker.GlobalStateValue(stack_type=pt.TealType.uint64)
    requester = beaker.GlobalStateValue(stack_type=pt.TealType.bytes)
    requestState = beaker.GlobalStateValue(
        stack_type=pt.TealType.uint64, 
        default=pt.Int(0))
    # 0-nothing | 1-requested | 2-approved | 3-rejected

app = beaker.Application("insurance", state=myState)

@app.create
def createApp(client: pt.abi.Account, *, output:pt.abi.String) -> pt.Expr:
    return pt.Seq(
        app.initialize_global_state(),
        app.state.requester.set(client.address()),
        output.set(client.address())
    )

@app.external(authorize=beaker.Authorize.only(app.state.requester.get()))
def registerAsset(
    name: pt.abi.String,
    desc: pt.abi.String,
    val: pt.abi.Uint64,
    *,
    output: pt.abi.String
) -> pt.Expr:
    return pt.Seq(
        app.state.requestState.set(pt.Int(1)),
        app.state.assetName.set(name.get()),
        app.state.assetDesc.set(desc.get()),
        app.state.assetVal.set(val.get()),
        output.set("Asset registrado con éxito."),
    )

@app.external(authorize=beaker.Authorize.only(pt.Global.creator_address()))
def approveAsset(tx:pt.abi.PaymentTransaction, *, output: pt.abi.String) -> pt.Expr:
    return pt.Seq(
        app.state.requestState.set(pt.Int(2)),
        pt.InnerTxnBuilder.Execute(
            {
                pt.TxnField.type_enum: pt.TxnType.AssetConfig,
                pt.TxnField.config_asset_unit_name: pt.Bytes("INS"),
                pt.TxnField.config_asset_name: pt.Bytes("INSURANCE"),
                pt.TxnField.config_asset_decimals: pt.Int(0),
                pt.TxnField.config_asset_total: pt.Int(1),
                pt.TxnField.note: pt.Concat(
                    pt.Bytes("Insurance token for asset: "),
                    app.state.assetName.get(),
                    pt.Bytes(" - Description: "),
                    app.state.assetDesc.get(),
                    pt.Bytes(" - Value: $"),
                    pt.Itob(app.state.assetVal.get()),
                ),
            }
        ),
        app.state.asaID.set(pt.InnerTxn.created_asset_id()),
        output.set(pt.Concat(
        pt.Bytes("Asset ID: "),
        pt.Itob(pt.InnerTxn.created_asset_id())
        ))
    )

@app.external(authorize=beaker.Authorize.only(app.state.requester.get()))
def claimInsurance(asa: pt.abi.Asset, *, output: pt.abi.String) -> pt.Expr:
    return pt.Seq(
        pt.InnerTxnBuilder.Execute(
            {
                pt.TxnField.type_enum: pt.TxnType.AssetTransfer,
                pt.TxnField.xfer_asset: asa.asset_id(),
                pt.TxnField.asset_receiver: pt.Txn.sender(),
                pt.TxnField.asset_amount: pt.Int(1),
            }
        ),
        app.state.assetName.set(pt.Bytes("")),
        app.state.assetDesc.set(pt.Bytes("")),
        app.state.assetVal.set(pt.Int(0)),
        app.state.requestState.set(pt.Int(0)),
        output.set("Token de seguro enviado")
    )


@app.external
def hello(name: pt.abi.String, *, output: pt.abi.String) -> pt.Expr:
    return output.set(pt.Concat(pt.Bytes("Hello, "), name.get()))
