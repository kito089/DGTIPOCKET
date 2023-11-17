document.addEventListener('DOMContentLoaded', function() {
	let index = 0;
	const noticias = document.querySelectorAll('.noticia');
  
	function mostrarSiguienteNoticia() {
	  noticias[index].classList.remove('active');
	  noticias[index].classList.add('anterior');
  
	  index = (index + 1) % noticias.length;
  
	  noticias[index].classList.add('active');
	  noticias[index].classList.remove('anterior');
	}
  
	setInterval(mostrarSiguienteNoticia, 3000); // Cambiar de noticia cada 3 segundos
  });
  