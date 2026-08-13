from .canonical import deep_copy
from .runtime import IVMRuntime
from .transaction import TransactionalCommitStore


class TransactionalIVMRuntime(IVMRuntime):
    """IVM v0.4 runtime for transactional commitment/recovery experiments."""

    def __init__(self, journal_path=None):
        super().__init__()
        self.store = TransactionalCommitStore(journal_path)

    def prepare_commit(self, *, process, event, state, transition):
        tx_id = self.store.transaction_id(
            process.process_id, event.event_id, state, transition
        )
        return self.store.prepare(tx_id, event.event_id, state, transition)

    def commit_with_history(self, *, transaction_id, history_id, moment_id):
        self.store.mark_state_committed(transaction_id)
        self.store.attach_history(transaction_id, history_id, moment_id)
        return self.store.finalize(transaction_id)

    def recover_transaction(self, transaction_id):
        return self.store.recover(transaction_id)
