const todos = [
  "Learn a new course",
  "Read a book",
  "Go to the gym",
  "Go shopping"
];
// Ex. 1: Atualiza a data no título quando o DOM for carregado
document.addEventListener("DOMContentLoaded", function () {
  const listDate = document.getElementById("list-date");

  function updateDate() {
    const today = new Date();
    listDate.textContent = today.toDateString();
  }

  updateDate(); // Chama a função para exibir a data
});

// Ex. 2: Renderiza a lista de tarefas


function renderTodoList() {
  const todoList = document.getElementById("todo-list");
  todoList.innerHTML = ""; // Limpa a lista antes de renderizar novamente

  todos.forEach((todo, index) => {
    const li = document.createElement("li");
    li.classList.add("todo-list-item");

    const p = document.createElement("p");
    p.textContent = todo;

    const deleteButton = document.createElement("button");
    deleteButton.textContent = "Delete";
    deleteButton.classList.add("delete-btn");

    // Ex. 5: Adiciona evento para remover a tarefa
    deleteButton.addEventListener("click", function () {
      removeTodoItem(index);
    });

    li.appendChild(p);
    li.appendChild(deleteButton);
    todoList.appendChild(li);
  });
}

// Ex. 3: Captura a submissão do formulário
document.addEventListener("DOMContentLoaded", function () {
  const todoForm = document.getElementById("todo-form");
  const taskInput = document.getElementById("task-input");

  todoForm.addEventListener("submit", function (event) {
    event.preventDefault(); // Evita o recarregamento da página
    const newTodo = taskInput.value.trim(); // Obtém o valor do input

    // Valida se a tarefa é única e não está vazia
    if (newTodo === "") {
      alert("Por favor, insira uma tarefa válida!");
      return;
    }
    if (todos.includes(newTodo)) {
      alert("Esta tarefa já está na lista!");
      return;
    }

    todos.push(newTodo); // Adiciona ao array
    taskInput.value = ""; // Limpa o input
    renderTodoList(); // Atualiza a lista de tarefas
  });
});

// Ex. 4: Função para remover todos os elementos filhos de um elemento pai
function removeAllChildNodes(parent) {
  while (parent.firstChild) {
    parent.removeChild(parent.firstChild);
  }
}

// Ex. 5 & 6: Remove uma tarefa e seu event listener associado
function removeTodoItem(index) {
  todos.splice(index, 1);
  renderTodoList();
}

// Inicializa a renderização da lista ao carregar a página
document.addEventListener("DOMContentLoaded", function () {
  renderTodoList();
});
