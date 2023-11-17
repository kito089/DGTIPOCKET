document.addEventListener('DOMContentLoaded', function() {
	let index = 0;
	const noticias = document.querySelectorAll('.noticia');
  
	function mostrarSiguienteNoticia() {
	  noticias[index].classList.remove('active');
	  noticias[index].style.opacity = 0;
	  
	  index = (index + 1) % noticias.length;
	  
	  noticias[index].classList.add('active');
	  noticias[index].style.opacity = 1;
	}
  
	setInterval(mostrarSiguienteNoticia, 2000); // Cambiar de noticia cada 3 segundos
  });
  
  