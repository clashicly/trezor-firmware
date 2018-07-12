# This file is part of the Trezor project.
#
# Copyright (C) 2012-2018 SatoshiLabs and contributors
#
# This library is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License version 3
# as published by the Free Software Foundation.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the License along with this library.
# If not, see <https://www.gnu.org/licenses/lgpl-3.0.html>.

import base64
import struct

from . import messages


def create_sign_tx(transaction) -> messages.RippleSignTx:
    if not all(transaction.get(k) for k in ("Fee", "Sequence", "TransactionType", "Amount", "Destination")):
        raise ValueError("Some of the required fields missing (Fee, Sequence, TransactionType, Amount, Destination")
    if transaction["TransactionType"] != "Payment":
        raise ValueError("Only Payment transaction type is supported")

    return messages.RippleSignTx(
        fee=transaction.get("Fee"),
        sequence=transaction.get("Sequence"),
        flags=transaction.get("Flags"),
        last_ledger_sequence=transaction.get("LastLedgerSequence"),
        payment=create_payment(transaction),
    )


def create_payment(transaction) -> messages.RipplePayment:
    return messages.RipplePayment(
        amount=transaction.get("Amount"),
        destination=transaction.get("Destination")
    )