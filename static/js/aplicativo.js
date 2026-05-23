/* ===============================================
   APLICATIVO LIFEAI - JAVASCRIPT PRINCIPAL
   =============================================== */

// ===============================================
// CONFIGURAÇÕES GLOBAIS
// ===============================================

const CONFIG = {
  TRANSICAO_RAPIDA: 300,
  TRANSICAO_MEDIA: 600,
  TRANSICAO_LENTA: 1000,
  URL_API: '/api',
  TEMPO_NOTIFICACAO: 5000,
  TAMANHO_MAXIMO_ARQUIVO: 10 * 1024 * 1024, // 10MB
  TIPOS_ARQUIVO_PERMITIDOS: ['image/jpeg', 'image/png', 'image/gif', 'image/webp']
};

// ===============================================
// INICIALIZAÇÃO
// ===============================================

document.addEventListener('DOMContentLoaded', function() {
  console.log('Inicializando LifeAI...');
  
  // Inicializar componentes
  inicializarCamposFormulario();
  inicializarBotoes();
  inicializarUploadExame();
  inicializarFiltros();
  inicializarTogglesSidebar();
  inicializarMenusDropdown();
  inicializarValidacaoFormularios();
  inicializarModais();
  
  console.log('LifeAI inicializado com sucesso!');
});

// ===============================================
// GERENCIAMENTO DE FORMULÁRIOS
// ===============================================

function inicializarCamposFormulario() {
  // Adicionar listeners para validação em tempo real
  const campos = document.querySelectorAll('input[type="email"], input[type="password"], input[type="text"]');
  
  campos.forEach(campo => {
    campo.addEventListener('blur', function() {
      validarCampo(this);
    });
    
    campo.addEventListener('focus', function() {
      limparErros(this);
    });
  });
}

function validarCampo(campo) {
  const tipo = campo.getAttribute('type');
  const valor = campo.value.trim();
  
  // Validar se o campo está vazio
  if (!valor) {
    mostrarErro(campo, 'Este campo é obrigatório');
    return false;
  }
  
  // Validar tipo específico
  switch(tipo) {
    case 'email':
      if (!validarEmail(valor)) {
        mostrarErro(campo, 'Email inválido');
        return false;
      }
      break;
      
    case 'password':
      if (valor.length < 6) {
        mostrarErro(campo, 'Senha deve ter no mínimo 6 caracteres');
        return false;
      }
      break;
  }
  
  removerErro(campo);
  return true;
}

function validarEmail(email) {
  const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return regex.test(email);
}

function mostrarErro(campo, mensagem) {
  // Remover erro anterior se existir
  removerErro(campo);
  
  // Adicionar classe de erro
  campo.classList.add('erro');
  
  // Criar elemento de mensagem de erro
  const elementoErro = document.createElement('span');
  elementoErro.className = 'mensagem-erro';
  elementoErro.textContent = mensagem;
  elementoErro.style.color = '#ad2e24';
  elementoErro.style.fontSize = '0.85rem';
  elementoErro.style.marginTop = '4px';
  elementoErro.style.display = 'block';
  
  campo.parentElement.appendChild(elementoErro);
}

function removerErro(campo) {
  campo.classList.remove('erro');
  const mensagem = campo.parentElement.querySelector('.mensagem-erro');
  if (mensagem) {
    mensagem.remove();
  }
}

function limparErros(campo) {
  campo.classList.remove('erro');
  const mensagem = campo.parentElement.querySelector('.mensagem-erro');
  if (mensagem) {
    mensagem.remove();
  }
}

// ===============================================
// GERENCIAMENTO DE BOTÕES
// ===============================================

function inicializarBotoes() {
  const botoes = document.querySelectorAll('.botao-primario, .botao-secundario, .botao-terciario');
  
  botoes.forEach(botao => {
    botao.addEventListener('click', function(e) {
      // Verificar se é um formulário
      const formulario = this.closest('form');
      if (formulario && this.type === 'submit') {
        if (!validarFormulario(formulario)) {
          e.preventDefault();
          return;
        }
      }
      
      // Adicionar animação de clique
      adicionarAnimacaoClique(this);
    });
  });
}

function validarFormulario(formulario) {
  const campos = formulario.querySelectorAll('input[required], textarea[required], select[required]');
  let valido = true;
  
  campos.forEach(campo => {
    if (!validarCampo(campo)) {
      valido = false;
    }
  });
  
  return valido;
}

function adicionarAnimacaoClique(elemento) {
  elemento.style.transform = 'scale(0.98)';
  setTimeout(() => {
    elemento.style.transform = 'scale(1)';
  }, CONFIG.TRANSICAO_RAPIDA / 2);
}

// ===============================================
// UPLOAD DE EXAME
// ===============================================

function inicializarUploadExame() {
  const areasUpload = document.querySelectorAll('.area-upload');
  
  areasUpload.forEach(area => {
    const inputArquivo = area.querySelector('input[type="file"]');
    
    if (!inputArquivo) {
      return;
    }
    
    // Drag and drop
    area.addEventListener('dragover', function(e) {
      e.preventDefault();
      e.stopPropagation();
      this.classList.add('ativa');
    });
    
    area.addEventListener('dragleave', function(e) {
      e.preventDefault();
      e.stopPropagation();
      this.classList.remove('ativa');
    });
    
    area.addEventListener('drop', function(e) {
      e.preventDefault();
      e.stopPropagation();
      this.classList.remove('ativa');
      
      const arquivos = e.dataTransfer.files;
      processarArquivos(arquivos, area);
    });
    
    // Clique para selecionar arquivo
    area.addEventListener('click', function() {
      inputArquivo.click();
    });
    
    // Mudança de arquivo via input
    inputArquivo.addEventListener('change', function() {
      processarArquivos(this.files, area);
    });
  });
}

function processarArquivos(arquivos, area) {
  if (arquivos.length === 0) {
    return;
  }
  
  const arquivo = arquivos[0];
  
  // Validar tipo de arquivo
  if (!CONFIG.TIPOS_ARQUIVO_PERMITIDOS.includes(arquivo.type)) {
    mostrarNotificacao('Tipo de arquivo não permitido. Use JPEG, PNG, GIF ou WebP.', 'erro');
    return;
  }
  
  // Validar tamanho do arquivo
  if (arquivo.size > CONFIG.TAMANHO_MAXIMO_ARQUIVO) {
    mostrarNotificacao('Arquivo muito grande. Tamanho máximo é 10MB.', 'erro');
    return;
  }
  
  // Ler arquivo
  const leitor = new FileReader();
  
  leitor.onload = function(e) {
    const imagem = e.target.result;
    exibirPreviewImagem(imagem, area);
    mostrarNotificacao('Imagem carregada com sucesso!', 'sucesso');
  };
  
  leitor.onerror = function() {
    mostrarNotificacao('Erro ao carregar a imagem.', 'erro');
  };
  
  leitor.readAsDataURL(arquivo);
}

function exibirPreviewImagem(imagem, area) {
  // Remover preview anterior se existir
  const previewAnterior = area.querySelector('.preview-imagem');
  if (previewAnterior) {
    previewAnterior.remove();
  }
  
  // Criar novo preview
  const preview = document.createElement('div');
  preview.className = 'preview-imagem';
  preview.innerHTML = `
    <img src="${imagem}" alt="Preview do exame">
    <button type="button" class="botao-remover-imagem" title="Remover imagem">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <line x1="18" y1="6" x2="6" y2="18"></line>
        <line x1="6" y1="6" x2="18" y2="18"></line>
      </svg>
    </button>
  `;
  
  // Inserir preview antes da área de upload (no mesmo contêiner)
  area.parentElement.insertBefore(preview, area);
  
  // Adicionar evento para remover
  const botaoRemover = preview.querySelector('.botao-remover-imagem');
  botaoRemover.addEventListener('click', function(e) {
    e.preventDefault();
    preview.remove();
    const inputArquivo = area.querySelector('input[type="file"]');
    if (inputArquivo) {
      inputArquivo.value = '';
    }
    mostrarNotificacao('Imagem removida.', 'info');
  });
}

// ===============================================
// FILTROS
// ===============================================

function inicializarFiltros() {
  const camposBusca = document.querySelectorAll('.campo-busca');
  
  camposBusca.forEach(campo => {
    // Debounce para evitar muitas requisições
    campo.addEventListener('input', debounce(function() {
      aplicarFiltros();
    }, CONFIG.TRANSICAO_RAPIDA));
  });
  
  // Filtros por select
  const selects = document.querySelectorAll('select[name*="filtro"]');
  selects.forEach(select => {
    select.addEventListener('change', function() {
      aplicarFiltros();
    });
  });
}

function aplicarFiltros() {
  const tabelas = document.querySelectorAll('table tbody');
  
  tabelas.forEach(tabela => {
    const linhas = tabela.querySelectorAll('tr');
    const campoBusca = document.querySelector('.campo-busca');
    const textoBusca = campoBusca ? campoBusca.value.toLowerCase() : '';
    
    linhas.forEach(linha => {
      const texto = linha.textContent.toLowerCase();
      const contem = texto.includes(textoBusca);
      
      linha.style.display = contem ? '' : 'none';
      
      if (contem) {
        linha.style.animation = 'fade-in 0.3s ease-out';
      }
    });
  });
}

function debounce(funcao, espera) {
  let timeout;
  return function executar(...argumentos) {
    clearTimeout(timeout);
    timeout = setTimeout(() => funcao.apply(this, argumentos), espera);
  };
}

// ===============================================
// SIDEBAR
// ===============================================

function inicializarTogglesSidebar() {
  const barraLateral = document.querySelector('.barra-lateral');
  const itensMenu = document.querySelectorAll('.barra-lateral .item-menu');
  
  // Marcar item ativo baseado na URL atual
  const urlAtual = window.location.pathname;
  itensMenu.forEach(item => {
    const link = item.querySelector('a');
    if (link && link.getAttribute('href') === urlAtual) {
      item.classList.add('ativo');
    } else {
      item.classList.remove('ativo');
    }
  });
}

// ===============================================
// MENUS DROPDOWN
// ===============================================

function inicializarMenusDropdown() {
  const acionadores = document.querySelectorAll('[data-toggle="dropdown"]');
  
  acionadores.forEach(acionador => {
    acionador.addEventListener('click', function(e) {
      e.preventDefault();
      e.stopPropagation();
      
      const menu = this.nextElementSibling;
      if (menu && menu.classList.contains('menu-dropdown')) {
        const aberto = menu.classList.contains('aberto');
        
        // Fechar outros menus abertos
        document.querySelectorAll('.menu-dropdown.aberto').forEach(m => {
          if (m !== menu) {
            m.classList.remove('aberto');
          }
        });
        
        // Alternar menu atual
        if (aberto) {
          menu.classList.remove('aberto');
        } else {
          menu.classList.add('aberto');
        }
      }
    });
  });
  
  // Fechar menus ao clicar fora
  document.addEventListener('click', function(e) {
    if (!e.target.closest('[data-toggle="dropdown"]') && !e.target.closest('.menu-dropdown')) {
      document.querySelectorAll('.menu-dropdown.aberto').forEach(menu => {
        menu.classList.remove('aberto');
      });
    }
  });
}

// ===============================================
// VALIDAÇÃO DE FORMULÁRIOS
// ===============================================

function inicializarValidacaoFormularios() {
  const formularios = document.querySelectorAll('form');
  
  formularios.forEach(formulario => {
    formulario.addEventListener('submit', function(e) {
      if (!validarFormulario(this)) {
        e.preventDefault();
      }
    });
  });
}

// ===============================================
// MODAIS
// ===============================================

function inicializarModais() {
  const botoesAbrir = document.querySelectorAll('[data-modal-target]');
  const botoesFechar = document.querySelectorAll('[data-modal-close]');
  
  // Abrir modais
  botoesAbrir.forEach(botao => {
    botao.addEventListener('click', function(e) {
      e.preventDefault();
      const idModal = this.getAttribute('data-modal-target');
      abrirModal(idModal);
    });
  });
  
  // Fechar modais
  botoesFechar.forEach(botao => {
    botao.addEventListener('click', function(e) {
      e.preventDefault();
      const modal = this.closest('.modal');
      if (modal) {
        fecharModal(modal.id);
      }
    });
  });
  
  // Fechar modal ao clicar fora
  document.querySelectorAll('.modal').forEach(modal => {
    modal.addEventListener('click', function(e) {
      if (e.target === this) {
        fecharModal(this.id);
      }
    });
  });
}

function abrirModal(idModal) {
  const modal = document.getElementById(idModal);
  if (modal) {
    modal.style.display = 'flex';
    modal.classList.add('aberto');
    document.body.style.overflow = 'hidden';
  }
}

function fecharModal(idModal) {
  const modal = document.getElementById(idModal);
  if (modal) {
    modal.classList.remove('aberto');
    setTimeout(() => {
      modal.style.display = 'none';
      document.body.style.overflow = '';
    }, CONFIG.TRANSICAO_RAPIDA);
  }
}

// ===============================================
// NOTIFICAÇÕES
// ===============================================

function mostrarNotificacao(mensagem, tipo = 'info') {
  const container = document.querySelector('.container-notificacoes') || criarContainerNotificacoes();
  
  const notificacao = document.createElement('div');
  notificacao.className = `notificacao notificacao-${tipo}`;
  notificacao.style.cssText = `
    background-color: ${obterCorNotificacao(tipo)};
    color: white;
    padding: 16px;
    border-radius: 8px;
    margin-bottom: 12px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    animation: slide-in 0.3s ease-out;
    word-wrap: break-word;
    max-width: 400px;
    font-weight: 500;
  `;
  notificacao.textContent = mensagem;
  
  container.appendChild(notificacao);
  
  // Remover após timeout
  setTimeout(() => {
    notificacao.style.animation = 'slide-out 0.3s ease-out';
    setTimeout(() => {
      notificacao.remove();
    }, CONFIG.TRANSICAO_RAPIDA);
  }, CONFIG.TEMPO_NOTIFICACAO);
}

function criarContainerNotificacoes() {
  const container = document.createElement('div');
  container.className = 'container-notificacoes';
  container.style.cssText = `
    position: fixed;
    top: 20px;
    right: 20px;
    z-index: 9999;
    display: flex;
    flex-direction: column;
    gap: 12px;
    max-height: calc(100vh - 40px);
    overflow-y: auto;
  `;
  document.body.appendChild(container);
  return container;
}

function obterCorNotificacao(tipo) {
  const cores = {
    sucesso: '#1f6f5a',
    erro: '#ad2e24',
    aviso: '#f0cf65',
    info: '#2dc2bd'
  };
  return cores[tipo] || cores.info;
}

// ===============================================
// ANÁLISE DE EXAME COM IA (SIMULAÇÃO)
// ===============================================

function inicializarAnaliseExame() {
  const botoesAnalisar = document.querySelectorAll('[data-analisar-exame]');
  
  botoesAnalisar.forEach(botao => {
    botao.addEventListener('click', async function(e) {
      e.preventDefault();
      
      const formulario = this.closest('form');
      if (!validarFormulario(formulario)) {
        mostrarNotificacao('Por favor, preencha todos os campos obrigatórios.', 'aviso');
        return;
      }
      
      await simularAnaliseIA(this);
    });
  });
}

async function simularAnaliseIA(botao) {
  // Desabilitar botão
  botao.disabled = true;
  const textoOriginal = botao.textContent;
  botao.textContent = 'Analisando...';
  
  try {
    // Simular processamento de 2-4 segundos
    const tempoProcessamento = Math.random() * 2000 + 2000;
    await aguardar(tempoProcessamento);
    
    // Gerar resultado aleatório
    const resultado = gerarResultadoAnalise();
    
    // Exibir resultado
    exibirResultadoAnalise(resultado);
    mostrarNotificacao('Análise concluída com sucesso!', 'sucesso');
    
  } catch (erro) {
    mostrarNotificacao('Erro ao analisar exame. Tente novamente.', 'erro');
    console.error(erro);
  } finally {
    botao.disabled = false;
    botao.textContent = textoOriginal;
  }
}

function aguardar(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

function gerarResultadoAnalise() {
  const prioridades = [
    { nivel: 'CRITICO', cor: '#ad2e24', risco: Math.random() * 30 + 70, gravidade: 'Crítica' },
    { nivel: 'URGENTE', cor: '#ff7a00', risco: Math.random() * 30 + 50, gravidade: 'Urgente' },
    { nivel: 'ATENCAO', cor: '#f0cf65', risco: Math.random() * 25 + 25, gravidade: 'Atenção' },
    { nivel: 'NORMAL', cor: '#1f6f5a', risco: Math.random() * 20 + 5, gravidade: 'Normal' }
  ];
  
  const prioridade = prioridades[Math.floor(Math.random() * prioridades.length)];
  
  const recomendacoes = [
    'Consulta imediata com radiologista',
    'Avaliação em 24 horas',
    'Acompanhamento rotineiro',
    'Nova avaliação em 3 meses'
  ];
  
  const temposEstimados = [
    '15-30 minutos',
    '30-60 minutos',
    '1-2 horas',
    'Agendado'
  ];
  
  return {
    gravidade: prioridade.gravidade,
    risco: Math.round(prioridade.risco),
    prioridade: prioridade.nivel,
    cor: prioridade.cor,
    recomendacao: recomendacoes[Math.floor(Math.random() * recomendacoes.length)],
    tempo: temposEstimados[Math.floor(Math.random() * temposEstimados.length)],
    confianca: Math.round(Math.random() * 10 + 90)
  };
}

function exibirResultadoAnalise(resultado) {
  // Localizar ou criar secao de resultado
  let secaoResultado = document.querySelector('.coluna-resultado');
  
  if (!secaoResultado) {
    secaoResultado = document.createElement('div');
    secaoResultado.className = 'coluna-resultado';
    document.querySelector('.container-novo-exame').appendChild(secaoResultado);
  }
  
  secaoResultado.innerHTML = `
    <div class="card-resultado">
      <div class="indicador-sucesso">
        <svg viewBox="0 0 100 100" fill="none">
          <circle class="circle-sucesso" cx="50" cy="50" r="45"></circle>
          <polyline class="checkmark" points="30,50 45,65 70,35"></polyline>
        </svg>
      </div>
      
      <div>
        <h3 class="titulo-resultado">Análise Concluída</h3>
        <p class="descricao-resultado">IA analisou o exame com sucesso</p>
      </div>
      
      <div class="bloco-resultado-principal">
        <div class="linha-resultado">
          <span class="label-resultado">Gravidade</span>
          <span class="valor-resultado">${resultado.gravidade}</span>
        </div>
        
        <div class="linha-resultado">
          <span class="label-resultado">Nível de Risco</span>
          <div class="indicador-percentual-resultado">
            <div class="barra-percentual">
              <div class="preenchimento-percentual" style="width: ${resultado.risco}%; background: linear-gradient(90deg, ${resultado.cor}, ${resultado.cor}80);"></div>
            </div>
            <span class="texto-percentual">${resultado.risco}%</span>
          </div>
        </div>
        
        <div class="linha-resultado">
          <span class="label-resultado">Prioridade</span>
          <span class="valor-resultado" style="color: ${resultado.cor};">${resultado.prioridade}</span>
        </div>
        
        <div class="linha-resultado">
          <span class="label-resultado">Confiança</span>
          <span class="valor-resultado">${resultado.confianca}%</span>
        </div>
      </div>
      
      <div class="secao-recomendacao">
        <h4 class="titulo-secao-resultado">Recomendação</h4>
        <p class="texto-recomendacao">${resultado.recomendacao}</p>
      </div>
      
      <div class="secao-tempo">
        <h4 class="titulo-secao-resultado">Tempo Estimado de Atendimento</h4>
        <p class="valor-tempo">${resultado.tempo}</p>
      </div>
      
      <div class="grupo-botoes-resultado">
        <button type="button" class="botao botao-primario" onclick="aprovarAnalise()">Aprovar Análise</button>
        <button type="button" class="botao botao-secundario" onclick="revisarAnalise()">Revisar</button>
      </div>
    </div>
  `;
}

function aprovarAnalise() {
  mostrarNotificacao('Análise aprovada e paciente adicionado à fila!', 'sucesso');
  // Aqui você poderia redirecionar ou limpar o formulário
}

function revisarAnalise() {
  mostrarNotificacao('Recarregando análise...', 'info');
  location.reload();
}

// ===============================================
// TABELAS RESPONSIVAS
// ===============================================

function inicializarTabelasResponsivas() {
  const tabelas = document.querySelectorAll('table');
  
  tabelas.forEach(tabela => {
    // Adicionar wrapper responsivo
    const wrapper = document.createElement('div');
    wrapper.className = 'tabela-responsiva';
    wrapper.style.overflowX = 'auto';
    tabela.parentNode.insertBefore(wrapper, tabela);
    wrapper.appendChild(tabela);
  });
}

// ===============================================
// ANIMAÇÕES DE ENTRADA
// ===============================================

function inicializarAnimacoesEntrada() {
  const elementos = document.querySelectorAll('[data-animacao]');
  
  if ('IntersectionObserver' in window) {
    const observador = new IntersectionObserver((entradas) => {
      entradas.forEach(entrada => {
        if (entrada.isIntersecting) {
          entrada.target.classList.add('animado');
          observador.unobserve(entrada.target);
        }
      });
    }, { threshold: 0.1 });
    
    elementos.forEach(elemento => {
      observador.observe(elemento);
    });
  } else {
    // Fallback para navegadores sem IntersectionObserver
    elementos.forEach(elemento => {
      elemento.classList.add('animado');
    });
  }
}

// ===============================================
// PAGINAÇÃO
// ===============================================

function inicializarPaginacao() {
  const botoesPaginacao = document.querySelectorAll('[data-pagina]');
  
  botoesPaginacao.forEach(botao => {
    botao.addEventListener('click', function(e) {
      e.preventDefault();
      const pagina = this.getAttribute('data-pagina');
      mudarPagina(pagina);
    });
  });
}

function mudarPagina(numeroPagina) {
  // Exemplo: esconder linhas da página anterior e mostrar da nova
  const tabelas = document.querySelectorAll('table tbody');
  const itensPorPagina = 10;
  
  tabelas.forEach(tabela => {
    const linhas = Array.from(tabela.querySelectorAll('tr'));
    const inicio = (numeroPagina - 1) * itensPorPagina;
    const fim = inicio + itensPorPagina;
    
    linhas.forEach((linha, indice) => {
      if (indice >= inicio && indice < fim) {
        linha.style.display = '';
        linha.style.animation = 'fade-in 0.3s ease-out';
      } else {
        linha.style.display = 'none';
      }
    });
  });
  
  // Atualizar botões ativos
  document.querySelectorAll('[data-pagina]').forEach(botao => {
    if (botao.getAttribute('data-pagina') === numeroPagina) {
      botao.classList.add('ativo');
    } else {
      botao.classList.remove('ativo');
    }
  });
}

// ===============================================
// CONFIGURAÇÕES - TOGGLES
// ===============================================

function inicializarToggleSwitches() {
  const toggles = document.querySelectorAll('.toggle-switch-pequeno input');
  
  toggles.forEach(toggle => {
    toggle.addEventListener('change', function() {
      const configuracao = this.getAttribute('data-configuracao');
      const valor = this.checked;
      
      // Aqui você poderia enviar para o servidor
      console.log(`Configuração ${configuracao} alterada para ${valor}`);
      mostrarNotificacao('Configuração atualizada com sucesso!', 'sucesso');
    });
  });
}

// ===============================================
// EXPORTAÇÃO
// ===============================================

function exportarParaPDF(nomeArquivo = 'relatorio.pdf') {
  // Isso requer uma biblioteca como jsPDF
  mostrarNotificacao('Funcionalidade de exportação em desenvolvimento', 'info');
}

function exportarParaExcel(nomeArquivo = 'dados.xlsx') {
  // Isso requer uma biblioteca como SheetJS
  mostrarNotificacao('Funcionalidade de exportação em desenvolvimento', 'info');
}

// ===============================================
// UTILITÁRIOS
// ===============================================

function formatarData(data) {
  const opcoes = { year: 'numeric', month: '2-digit', day: '2-digit' };
  return new Date(data).toLocaleDateString('pt-BR', opcoes);
}

function formatarHora(hora) {
  const opcoes = { hour: '2-digit', minute: '2-digit' };
  return new Date(hora).toLocaleTimeString('pt-BR', opcoes);
}

function formatarDataHora(dataHora) {
  return `${formatarData(dataHora)} às ${formatarHora(dataHora)}`;
}

// ===============================================
// INICIALIZAR ANÁLISE DE EXAME
// ===============================================

document.addEventListener('DOMContentLoaded', function() {
  inicializarAnaliseExame();
  inicializarTabelasResponsivas();
  inicializarAnimacoesEntrada();
  inicializarPaginacao();
  inicializarToggleSwitches();
});

// Exportar funções para uso global
window.mostrarNotificacao = mostrarNotificacao;
window.abrirModal = abrirModal;
window.fecharModal = fecharModal;
window.aprovarAnalise = aprovarAnalise;
window.revisarAnalise = revisarAnalise;
window.exportarParaPDF = exportarParaPDF;
window.exportarParaExcel = exportarParaExcel;
