client_list = [
    {
        "name": "Maria Silva",
        "cpf": "1",
        "password": "0",
        "payment_history": "Good history so far, but with recent delay in the last 2 installments of real estate financing and multiple personal loans.",
        "debts": {
            "real_estate_financing": {
                "installment_value": 3500.00,
                "overdue_installments": [
                    {"value": 3500.00},
                    {"value": 3500.00},
                    {"value": 3500.00}
                ],
            },
            "personal_loan": {
                "installment_value": 1500.00,
                "overdue_installments": [
                    {"value": 1500.00},
                    {"value": 1500.00},
                    {"value": 1500.00}
                ],
            },
            "payroll_loan": {
                "installment_value": 900.00,
                "overdue_installments": []
        },
        "consent_obtained": False,
        "identity_confirmed": False
        }
    },
    {
        "name": "João Oliveira",
        "cpf": "2",
        "password": "0",
        "payment_history": "Excellent history, always on time with all payments.",
        "debts": {},
        "consent_obtained": False,
        "identity_confirmed": False
    },
    {
        "name": "Pedro Santos",
        "cpf": "3",
        "25/12/1990"
        "payment_history": "Some delays in credit card payments in the past year, but currently stable.",
        "debts": {
            "credit_card": {
                "installment_value": 0,
                "overdue_installments": [
                    {"value": 1750.00}
                ],
                "status": "Overdue"
            }
        },
        "consent_obtained": False,
        "identity_confirmed": False
    },
    {
        "name": "Ana Souza",
        "cpf": "4",
        "password": "0",
        "payment_history": "Perfect payment history, no debts.",
        "debts": {},
        "consent_obtained": False,
        "identity_confirmed": False
    },
    {
        "name": "Carla Lima",
        "cpf": "5",
        "password": "0",
        "payment_history": "Frequent delays in utility bills and a pending car loan installment.",
        "debts": {
            "car_loan": {
                "installment_value": 800.00,
                "overdue_installments": [
                    {"value": 800.00}
                ],
            },
            "utility_bills": {
                "installment_value": 300.00,
                "overdue_installments": [
                    {"value": 300.00}
                ],
            }
        },
        "consent_obtained": False,
        "identity_confirmed": False
    }
]

client_by_doc_number = {client["cpf"]: client for client in client_list}