from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from client_mock import client_by_doc_number

llm = None

def set_llm(key):
    global llm

    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.4, google_api_key=key)

bank_rules_text = """
Regras de Negociação Banco Confiança:
1. Financiamento Imobiliário:
    - Em atraso: A partir de 60 dias.
    - Opções:
      - Parcelamento de Dívida Vencida: Até 24x, juros de 0.5% a.m. sobre o valor renegociado.
      - Extensão de Prazo: Até 12 meses no prazo total, redução da parcela (ex: RS 3500 para RS 3000).
      - Desconto para Quitação Total: 10% sobre o valor em atraso.
      - Entrada Mínima: 10% do valor em atraso.
2. Empréstimos Pessoais (Múltiplos):
    - Em atraso: A partir de 30 dias.
    - Opções:
      - Unificação de Dívidas: Até 36x, juros de 1.5% a.m. sobre o valor unificado.
      - Desconto para Quitação Total: 15% sobre o valor em atraso.
3. Empréstimo Consignado:
    - Status: Geralmente em dia, pouca margem para renegociação de valores ou juros.
    - Ação do Agente: Reconhecer sua existência, mas focar em outras dívidas.

Lembre-se de sempre apresentar os valores e condições de forma clara e transparente.
"""

def get_client_profile_for_prompt(client_data):

    debts = [
        f"""
        - { name }:
            - Parcela: RS {'Valor Variável' if data['installment_value'] == -1 else data['installment_value']:.2f}/mês
            - Parcelas em Atraso: {len(data['overdue_installments'])}
            - Valor Total em Atraso (incluindo juros/multas): RS {sum(overdue["value"] for overdue in data['overdue_installments']):.2f}
            - Status: {'Overdue' if data['overdue_installments'] else 'Up to date'}
        """ for name, data in client_data['debts'].items() if data
    ]
    
    profile_str = f"""
    Dados do Cliente:
    - Nome: {client_data['name']}
    - CPF: {client_data['cpf']}
    - Histórico de Pagamento: {client_data['payment_history']}

    Dívidas Atuais:
    { '\n'.join(debts)}
    """

    print(profile_str)
    return profile_str

def create_agent_chain(client_data):
    agent_prompt = ChatPromptTemplate.from_messages([
        ("system", f"""
        Você é o **Assistente Inteligente de Renegociação** do "Banco Confiança".
        Seu objetivo é ajudar clientes inadimplentes a entender sua situação e fechar acordos de renegociação de dívidas de forma **empática, respeitosa, clara e proativa**.

        **Restrições e Diretrizes Essenciais:**
        - **Empatia e Respeito:** Utilize sempre um tom acolhedor, compreensivo e sem julgamentos. Reconheça a dificuldade da situação do cliente.
        - **Clareza:** Use linguagem simples, evite jargões financeiros complexos.
        - **Proatividade:** Ofereça soluções e guie o cliente para os próximos passos.
        - **Foco na Solução:** O objetivo é levar a um acordo de renegociação.
        - **Segurança e Dados:** Nunca peça dados sensíveis (senhas, número de cartão) além do CPF para identificação inicial. O consentimento e CPF já foram obtidos e confirmados para esta conversa. Nunca forneça dados pessoais como CPF, senha e outros.
        - **Regras do Banco Confiança:**
          {bank_rules_text}

        **Contexto do Cliente:**
        {get_client_profile_for_prompt(client_data)}

        Sempre considere o histórico da conversa para manter o contexto e a continuidade.
        """),
        MessagesPlaceholder(variable_name="chat_history"),
        ("user", "{input}")
    ])
    return agent_prompt | llm

def process_agent_message(user_input, chat_history, current_client_data):
    agent_response = ""

    if not current_client_data:
        if client:=client_by_doc_number.get(user_input):
            current_client_data = client
            agent_response = "Olá! Para que eu possa continuar te ajudando, preciso do seu consentimento explícito para prosseguir com este atendimento via chatbot. Por favor, digite SIM se você concorda em continuar."
        else:
            agent_response = "Não consegui identificar seu cadastro, tente inserir seu CPF novamente, que tal inserir um número de 1 a 5?"

    elif not current_client_data.get("consent_obtained"):
        if user_input.upper() == "SIM":
            current_client_data["consent_obtained"] = True
            agent_response = "Ótimo! Para sua segurança, preciso confirmar alguns dados. Por favor, digite sua senha (é 0)."
        else:
            agent_response = "Entendo. Se precisar de ajuda no futuro, estarei disponível. Tenha um bom dia!"

    elif not current_client_data.get("identity_confirmed"):
        if user_input == current_client_data["password"]:
            current_client_data["identity_confirmed"] = True
            agent_response = f"Obrigada, Sr(a). {current_client_data['name']}. Agora que confirmamos sua identidade e temos seu consentimento, posso informar que temos condições especiais para você regularizar suas contas, especificamente em relação ao seu **Financiamento Imobiliário** e seus **empréstimos ativos**. Sabemos que lidar com dívidas não é fácil, e dado o seu histórico conosco, queremos muito te ajudar a encontrar a melhor solução. Podemos conversar sobre as opções que temos para você?"
        else:
            agent_response = "Senha inválida. Por favor, digite seu sua senha novamente para prosseguir."
    else:
        chain = create_agent_chain(current_client_data)
        llm_response = chain.invoke({
            "input": user_input,
            "chat_history": chat_history
        })
        agent_response = llm_response.content.replace('$', r'\$').replace(r'\\$', r'\$')

    return agent_response, current_client_data

def get_first_message():
    return "Olá! Sou o Renê da Renegoc.IA, assistente virtual parceiro do Banco Confiança e estou aqui para te ajudar a organizar suas finanças. Para prosseguir, preciso que você informe seu numero de identificação (mock de 1 a 5)"