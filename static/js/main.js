document.addEventListener("DOMContentLoaded", function () {
  console.log("JavaScript is successfully loaded and running!");
});

document.addEventListener("DOMContentLoaded", () => {
  let draggedElement = null;
  const tableBody = document.querySelector("tbody");

  if (!tableBody) return; // Se a tabela não existir, sai

  // -----------------------------------------------------
  // FUNÇÕES DE EVENTOS DE DRAG
  // -----------------------------------------------------

  // 1. O que acontece quando o arrastar começa
  const handleDragStart = (e) => {
    draggedElement = e.target.closest("tr");
    if (!draggedElement || !draggedElement.classList.contains("draggable"))
      return;

    draggedElement.classList.add("dragging");
    // Define o tipo de dado que está a ser arrastado (necessário para Firefox)
    e.dataTransfer.setData("text/plain", draggedElement.dataset.id);
  };

  // 2. O que acontece quando o elemento está sobre outro
  const handleDragOver = (e) => {
    e.preventDefault(); // Necessário para permitir o drop
    if (!draggedElement || !e.target.closest("tr")) return;

    const currentTargetRow = e.target.closest("tr");
    if (currentTargetRow === draggedElement) return;

    // Feedback visual: determina se a linha de inserção deve ser acima ou abaixo
    const rect = currentTargetRow.getBoundingClientRect();
    const y = e.clientY - rect.top;

    if (y < rect.height / 2) {
      // Mouse na metade superior: inserir acima
      currentTargetRow.classList.add("drop-zone-indicator");
      currentTargetRow.classList.remove("drop-zone-indicator-bottom");
    } else {
      // Mouse na metade inferior: inserir abaixo
      currentTargetRow.classList.add("drop-zone-indicator-bottom");
      currentTargetRow.classList.remove("drop-zone-indicator");
    }
  };

  // 3. O que acontece quando o drag sai de cima de um elemento
  const handleDragLeave = (e) => {
    const target = e.target.closest("tr");
    if (target) {
      target.classList.remove(
        "drop-zone-indicator",
        "drop-zone-indicator-bottom"
      );
    }
  };

  // 4. O que acontece quando o arrastar termina
  const handleDragEnd = (e) => {
    e.target.classList.remove("dragging");
    // Remove todos os indicadores de drop
    document
      .querySelectorAll(".drop-zone-indicator, .drop-zone-indicator-bottom")
      .forEach((el) => {
        el.classList.remove(
          "drop-zone-indicator",
          "drop-zone-indicator-bottom"
        );
      });
    draggedElement = null;
  };

  // 5. O que acontece quando o elemento é solto
  const handleDrop = (e) => {
    e.preventDefault();

    if (!draggedElement || !e.target.closest("tr")) return;

    const droppedTargetRow = e.target.closest("tr");

    if (droppedTargetRow === draggedElement) return;

    // Limpa os indicadores
    droppedTargetRow.classList.remove(
      "drop-zone-indicator",
      "drop-zone-indicator-bottom"
    );

    // Determina onde inserir o elemento
    if (droppedTargetRow.classList.contains("drop-zone-indicator")) {
      // Inserir antes do alvo
      tableBody.insertBefore(draggedElement, droppedTargetRow);
    } else {
      // Inserir depois do alvo
      tableBody.insertBefore(draggedElement, droppedTargetRow.nextSibling);
    }

    // -----------------------------------------------------
    // LÓGICA DE ATUALIZAÇÃO DO SERVIDOR (AJAX)
    // -----------------------------------------------------
    const newOrder = Array.from(tableBody.children).map((row, index) => ({
      id: row.dataset.id,
      ordem: index, // O novo índice (ordem) na lista
    }));

    // Esta função precisa ser implementada para enviar 'newOrder' para uma View Django via fetch/AJAX
    // Enviar esta lista 'newOrder' para o backend para salvar a nova ordem
    // saveNewTaskOrder(newOrder);
    console.log("Nova ordem a ser enviada para o Django:", newOrder);

    handleDragEnd(e); // Termina a operação
  };

  // -----------------------------------------------------
  // REGISTAR LISTENERS
  // -----------------------------------------------------
  document.querySelectorAll(".draggable").forEach((item) => {
    item.addEventListener("dragstart", handleDragStart);
    item.addEventListener("dragend", handleDragEnd);
  });

  // Os eventos DragOver e Drop precisam ser no elemento pai (tbody)
  tableBody.addEventListener("dragover", handleDragOver);
  tableBody.addEventListener("dragleave", handleDragLeave);
  tableBody.addEventListener("drop", handleDrop);
});
