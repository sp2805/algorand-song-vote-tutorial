from ast import Assert, Global, If, Return

from traitlets import Int
from pyteal import * # type: ignore
import os

"""Basic Counter Application"""

def approval_program():
    handle_creation = Seq( # type: ignore
        App.globalPut(Bytes("Count1"), Int(0)), # type: ignore
        App.globalPut(Bytes("Count2"), Int(0)), # type: ignore
        App.globalPut(Bytes("Count3"), Int(0)), # type: ignore
        Return(Int(1))
    )
    # handle creation function above
    handle_optin = Return(Int(0))
    handle_closeout = Return(Int(0))
    handle_updateapp = Return(Int(0))
    handle_deleteapp = Return(Int(0))
    # conditional statement below
    # delete app above
    scratchCount = ScratchVar(TealType.uint64) # type: ignore
    addC1 = Seq( # type: ignore
        scratchCount.store(App.globalGet(Bytes("Count1"))), # type: ignore
        App.globalPut(Bytes("Count1"), scratchCount.load() + Int(1)), # type: ignore
        Return(Int(1))
    )
    addC2 = Seq( # type: ignore
        scratchCount.store(App.globalGet(Bytes("Count2"))), # type: ignore
        App.globalPut(Bytes("Count2"), scratchCount.load() + Int(1)), # type: ignore
        Return(Int(1))
    )
    addC3 = Seq( # type: ignore
        scratchCount.store(App.globalGet(Bytes("Count3"))), # type: ignore
        App.globalPut(Bytes("Count3"), scratchCount.load() + Int(1)), # type: ignore
        Return(Int(1))
    )
    deduct = Seq([ # type: ignore
        scratchCount.store(App.globalGet(Bytes("Count"))), # type: ignore
        If(scratchCount.load() > Int(0),
            App.globalPut(Bytes("Count"), scratchCount.load() - Int(1)), # type: ignore
        ),
        Return(Int(1))
    ])
    handle_noop = Seq( # type: ignore
        # First, fails immediately if this transaction is grouped with others
        Assert(Global.group_size() == Int(1)),
        Cond( # type: ignore
            [Txn.application_args[0] == Bytes("AddC1"), addC1], # type: ignore
            [Txn.application_args[0] == Bytes("AddC2"), addC2], # type: ignore
            [Txn.application_args[0] == Bytes("AddC3"), addC3] # type: ignore
        )
    )
    # conditional below
    program = Cond( # type: ignore
        [Txn.application_id() == Int(0), handle_creation], # type: ignore
        [Txn.on_completion() == OnComplete.OptIn, handle_optin], # type: ignore
        [Txn.on_completion() == OnComplete.CloseOut, handle_closeout], # type: ignore
        [Txn.on_completion() == OnComplete.UpdateApplication, handle_updateapp], # type: ignore
        [Txn.on_completion() == OnComplete.DeleteApplication, handle_deleteapp], # type: ignore
        [Txn.on_completion() == OnComplete.NoOp, handle_noop] # type: ignore
    )
    return compileTeal(program, Mode.Application, version=5) # type: ignore

def clear_state_program():
    program = Return(Int(1))
    return compileTeal(program, Mode.Application, version=5) # type: ignore

if __name__ == "__main__":
    path = "./contracts/artifacts"
    with open(os.path.join(path, "songvote_approval.teal"), 'w') as f:
        f.write(approval_program())
    with open(os.path.join(path, "songvote_clear.teal"), 'w') as f:
        f.write(clear_state_program())