from bottle import route, run, template, request, redirect, static_file

# -----------------------------
# Dados em memória (simples)
# -----------------------------
planos = [
    {"id": 1, "nome": "Plano Básico", "descricao": "Acesso simples"},
    {"id": 2, "nome": "Plano Premium", "descricao": "Acesso total"},
]

next_id = 3

# -----------------------------
# STATIC
# -----------------------------
@route('/static/<filename:path>')
def server_static(filename):
    return static_file(filename, root='static')


# -----------------------------
# ROTA INICIAL
# -----------------------------
@route('/')
def home():
    return "<h2>Sistema funcionando!</h2><a href='/login'>Ir para Login</a>"


# -----------------------------
# LOGIN
# -----------------------------
@route('/login')
def login_form():
    return template("login")


@route('/login', method='POST')
def login_submit():
    usuario = request.forms.get("usuario")
    senha = request.forms.get("senha")

    if usuario == "admin" and senha == "123":
        redirect('/planos')
    else:
        return "<h2>Login inválido</h2><a href='/login'>Tentar novamente</a>"


# -----------------------------
# LISTAR PLANOS
# -----------------------------
@route('/planos')
def listar():
    return template("clientes", lista=planos)


# -----------------------------
# FORM CRIAR
# -----------------------------
@route('/planos/novo')
def novo_form():
    return template("form", registro=None, modo="novo")


@route('/planos/novo', method='POST')
def novo_submit():
    global next_id
    nome = request.forms.get("nome")
    descricao = request.forms.get("descricao")

    planos.append({"id": next_id, "nome": nome, "descricao": descricao})
    next_id += 1

    redirect('/planos')


# -----------------------------
# EDITAR
# -----------------------------
@route('/planos/editar/<id:int>')
def editar_form(id):
    for p in planos:
        if p["id"] == id:
            return template("form", registro=p, modo="editar")
    return "Registro não encontrado."


@route('/planos/editar/<id:int>', method='POST')
def editar_submit(id):
    nome = request.forms.get("nome")
    descricao = request.forms.get("descricao")

    for p in planos:
        if p["id"] == id:
            p["nome"] = nome
            p["descricao"] = descricao
            break

    redirect('/planos')


# -----------------------------
# EXCLUIR
# -----------------------------
@route('/planos/excluir/<id:int>')
def excluir(id):
    global planos
    planos = [p for p in planos if p["id"] != id]
    redirect('/planos')


# -----------------------------
# RUN
# -----------------------------
run(host='localhost', port=8080, debug=True)
