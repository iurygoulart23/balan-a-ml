var barra_class = "nav-area nav-top-area nav-center-area";
var barra_busca = document.getElementsByClassName(barra_class);

// Verifica se algum elemento foi encontrado
if (barra_busca.length > 0) {
    // Supondo que o campo de busca seja o primeiro elemento encontrado
    var campo_busca = barra_busca[0];

    // Encontrar o elemento input dentro do campo de busca
    var input_busca = campo_busca.querySelector('input');

    // Verifica se o elemento input existe
    if (input_busca) {
        input_busca.value = "balança"; // Insere a palavra "balança" no campo de busca
    } else {
        console.error('Elemento input não encontrado dentro da barra de busca.');
    }
} else {
    console.error('Nenhum elemento com a classe especificada foi encontrado.');
}

document.getElementsByClassName('nav-search-btn')[0].click()