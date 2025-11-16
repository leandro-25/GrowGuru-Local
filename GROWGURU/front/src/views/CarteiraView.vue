<template>
  <ion-page class="carteira-page">
    <ion-header class="ion-no-border">
      <ion-toolbar>
        <div class="header-container">
          <div class="logo-container">
            <img src="@/assets/imagem/logoPPP.png" alt="Logo" class="logo-image" />
            <div class="brand-text">
              <span class="brand-bold">Carteira</span>
            </div>
          </div>

        </div>
      </ion-toolbar>
    </ion-header>

    <ion-content>
      <!-- Estado de carregamento -->
      <div v-if="carregando" class="loading-container">
        <ion-spinner name="crescent"></ion-spinner>
        <p>Carregando sua carteira...</p>
      </div>

      <!-- Conteúdo principal -->
      <div v-else>
        <!-- Resumo da carteira -->
        <div class="resumo-container">
          <div class="valor-total">
            <h2>Valor Total</h2>
            <p class="valor">{{ formatarMoeda(valorTotalCarteira) }}</p>
          </div>
        </div>

        <!-- Gráfico de Distribuição -->
        <div v-if="carteira.length > 0" class="chart-section">
          <div class="chart-container">
            <canvas ref="chartRef" width="100%" height="100%"></canvas>
          </div>
          <!-- Carrossel de Legenda -->
          <div class="carousel-container" @mouseenter="pausarCarrossel" @mouseleave="retomarCarrossel"
            @touchstart="toqueInicio" @touchend="toqueFim">
            <div ref="legendCarousel" class="legend-container" :class="{ 'paused': carrosselPausado }">
              <div v-for="(item, index) in legendasDuplicadas" :key="`${index}-${item.nome}`" class="legend-item">
                <div class="legend-icon"
                  :class="`legend-icon-${(carteira.findIndex(i => i.nome === item.nome) % 20) + 1}`"
                  :style="{ backgroundColor: item.cor }"></div>
                <span class="legend-text">{{ item.nome }}</span>
              </div>
            </div>
          </div>
        </div>

        <div v-else class="empty-state">
          <!--<ion-icon name="wallet-outline" size="large"></ion-icon>-->
          <p>Nenhum investimento encontrado</p>
          <ion-button @click="irParaInvestir" class="add-button">
            Adicionar Investimento
          </ion-button>
        </div>

        <!-- Lista de Estratégias -->
        <!-- Modern Strategy List -->
        <div v-if="carteira.length > 0" class="modern-strategy-list">
          <div v-for="estrategia in carteira" :key="estrategia.id" class="strategy-card"
            :class="{ 'expanded': estrategia.aberto }">
            <!-- Strategy Header -->
            <div class="strategy-header" @click="toggleDetalhes(estrategia.id)">
              <div class="strategy-header-content">
                <!--<div class="strategy-icon">
                  <ion-icon :name="estrategia.aberto ? 'folder-open' : 'folder'" class="folder-icon"></ion-icon>
                </div>-->
                <div class="strategy-info">
                  <h3 class="strategy-name">{{ estrategia.nome }}</h3>
                  <div class="strategy-meta">
                    <span class="strategy-percentage">{{ estrategia.porcentagem }}%</span>
                    <span class="strategy-value">{{ formatarMoeda(estrategia.total_investido) }}</span>
                  </div>
                </div>
                <!--<ion-icon :icon="estrategia.aberto ? chevronDown : chevronForward" class="toggle-arrow"></ion-icon>-->
              </div>

              <!-- Progress Bar -->
              <div class="progress-container">
                <div class="progress-bar" :style="{ width: `${estrategia.porcentagem}%` }"></div>
              </div>
            </div>

            <!-- Assets List (Visible when expanded) -->
            <transition name="slide-fade">
              <div v-if="estrategia.aberto" class="assets-container">
                <div v-for="ativo in estrategia.ativos" :key="ativo.codigo" class="asset-card">
                  <!-- Asset Header -->
                  <div class="asset-header">
                    <div class="asset-symbol">
                      <span class="symbol-badge">{{ ativo.codigo }}</span>
                      <span class="profit-badge"
                        :class="{ 'profit': calcularLucro(ativo) >= 0, 'loss': calcularLucro(ativo) < 0 }">
                        {{ calcularLucro(ativo) }}%
                      </span>
                    </div>
                    <div class="asset-value">
                      {{ formatarMoeda(ativo.quantidade * ativo.valor_medio) }}
                    </div>
                  </div>

                  <!-- Asset Details Grid -->
                  <div class="asset-details">
                    <!-- First Row -->
                    <div class="detail-item">
                      <!--<ion-icon name="calculator-outline" class="detail-icon"></ion-icon>-->
                      <div class="detail-content">
                        <span class="detail-label">Quantidade</span>
                        <span class="detail-value">{{ ativo.quantidade }} un</span>
                      </div>
                    </div>
                    <div class="detail-item">
                      <!--<ion-icon name="pricetag-outline" class="detail-icon"></ion-icon>-->
                      <div class="detail-content">
                        <span class="detail-label">Preço Médio</span>
                        <span class="detail-value">{{ formatarMoeda(ativo.valor_medio) }}</span>
                      </div>
                    </div>
                    <!-- Second Row -->
                    <div class="detail-item">
                      <!--<ion-icon name="trending-up-outline" class="detail-icon"></ion-icon>-->
                      <div class="detail-content">
                        <span class="detail-label">Valor Atual</span>
                        <span class="detail-value">{{ formatarMoeda(ativo.preco_atual || ativo.valor_medio) }}</span>
                      </div>
                    </div>
                    <div class="detail-item">
                      <!--<ion-icon name="wallet-outline" class="detail-icon"></ion-icon>-->
                      <div class="detail-content">
                        <span class="detail-label">Total Investido</span>
                        <span class="detail-value">{{ formatarMoeda(ativo.quantidade * ativo.valor_medio) }}</span>
                      </div>
                    </div>
                  </div>

                  <!-- Sell Action -->
                  <div class="asset-actions">
                    <div class="action-inputs">
                      <div class="input-group">
                        <label>Quantidade</label>
                        <ion-input v-model="ativo.quantidadeVenda" type="number" :min="0" :max="ativo.quantidade"
                          placeholder="0" class="modern-input"></ion-input>
                      </div>
                      <div class="input-group">
                        <label>Preço Unitário</label>
                        <ion-input v-model.number="ativo.precoVenda" type="number" :min="0" step="0.01"
                          :placeholder="formatarMoeda(ativo.valor_medio || 0, true)" class="modern-input"></ion-input>
                      </div>
                    </div>
                    <ion-button @click.stop="venderAtivo(ativo, estrategia.id)" expand="block" class="sell-button"
                      :disabled="!ativo.quantidadeVenda || ativo.quantidadeVenda <= 0">
                      <!--<ion-icon :icon="cashOutline" slot="start"></ion-icon>-->
                      Vender Ativo
                    </ion-button>
                  </div>
                </div>
              </div>
            </transition>
          </div>
        </div>
      </div>
    </ion-content>
  </ion-page>
</template>

<script setup>
import { ref, onMounted, nextTick, computed, onBeforeUnmount, watch } from 'vue';
import { useRouter } from 'vue-router';
import { Chart, registerables } from 'chart.js';
import { DoughnutController, ArcElement, Tooltip, Legend } from 'chart.js';

// Registra os componentes necessários do Chart.js
Chart.register(...registerables, DoughnutController, ArcElement, Tooltip, Legend);
import { chevronDown, chevronForward, refreshOutline } from 'ionicons/icons';
import { toastController } from '@ionic/vue';
import { api } from '@/api';

import {
  IonButton,
  IonInput,
  IonLabel,
  IonPage,
  IonHeader,
  IonToolbar,
  IonTitle,
  IonContent,
  IonList,
  IonItem,
  IonItemGroup,
  IonIcon,
  IonButtons,
  IonBackButton,
  IonSpinner
} from '@ionic/vue';

const router = useRouter();
const carregando = ref(true);
const carteira = ref([]);
const chartRef = ref(null);
const chartInstance = ref(null);
const carrosselPausado = ref(false);
const legendCarousel = ref(null);
let touchStartX = 0;
let touchEndX = 0;
let carrosselInterval = null;
const legendasDuplicadas = ref([]);
let pollingInterval = null;

const coresGrafico = [
  '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF',
  '#FF9F40', '#C9CB3F', '#FF6F61', '#6B7280', '#34D399',
  '#F472B6', '#10B981', '#60A5FA', '#FBBF24', '#EC4899',
  '#4ADE80', '#F87171', '#38BDF8', '#A78BFA', '#FCD34D'
];

const valorTotalCarteira = computed(() => {
  return carteira.value.reduce((total, estrategia) => total + estrategia.total_investido, 0);
});

const formatarMoeda = (valor) => {
  return new Intl.NumberFormat('pt-BR', {
    style: 'currency',
    currency: 'BRL'
  }).format(valor);
};

const calcularLucro = (ativo) => {
  if (!ativo?.valor_medio || !ativo?.preco_atual) return '0.00';
  const lucro = ((ativo.preco_atual - ativo.valor_medio) / ativo.valor_medio) * 100;
  return lucro.toFixed(2);
};

const toggleDetalhes = (id) => {
  carteira.value = carteira.value.map(e => ({
    ...e,
    aberto: e.id === id ? !e.aberto : e.aberto
  }));
};

const venderAtivo = async (ativo, estrategiaId) => {
  try {
    if (!ativo.quantidadeVenda || ativo.quantidadeVenda <= 0) {
      mostrarMensagem('Informe uma quantidade válida para venda', 'warning');
      return;
    }

    if (ativo.quantidadeVenda > ativo.quantidade) {
      mostrarMensagem('Quantidade solicitada maior que a disponível', 'warning');
      return;
    }

    const loadingMessage = await mostrarMensagem('Processando venda...', 'primary', true);

    // Verifica se o preço de venda foi informado
    const precoVenda = ativo.precoVenda || ativo.preco_atual || ativo.valor_medio;
    if (!precoVenda) {
      mostrarMensagem('Informe um preço de venda válido', 'warning');
      return;
    }

    // Realiza a venda com o preço informado pelo usuário
    await api.post('/vender', {
      codigo_ativo: ativo.codigo,
      estrategia_id: estrategiaId,
      quantidade: parseFloat(ativo.quantidadeVenda),
      preco_venda: parseFloat(precoVenda) // Adiciona o preço de venda
    });

    // Atualiza os dados da carteira mantendo o estado de expansão
    const response = await api.get('/carteira');

    // Mantém o estado de abertura das estratégias
    const estrategiasAbertas = new Set(
      carteira.value
        .filter(e => e.aberto)
        .map(e => e.id)
    );

    // Atualiza a carteira mantendo o estado de abertura
    carteira.value = response.data.map(estrategia => ({
      ...estrategia,
      aberto: estrategiasAbertas.has(estrategia.id),
      ativos: (estrategia.ativos || []).map(ativo => ({
        ...ativo,
        quantidadeVenda: 0,
        precoVenda: ativo.valor_medio || ativo.preco_atual || 0,
        codigo: ativo.codigo || ativo.codigo_ativo
      }))
    }));

    // Atualiza o gráfico
    await nextTick();
    if (carteira.value.length > 0) {
      atualizarGrafico();
    }

    loadingMessage.dismiss();
    mostrarMensagem('Venda realizada com sucesso!', 'success');

  } catch (error) {
    console.error('Erro ao vender ativo:', error);
    mostrarMensagem('Erro ao processar venda', 'danger');
  }
};

const atualizarDados = async () => {
  carregando.value = true;
  await carregarCarteira();
  mostrarMensagem('Dados atualizados!', 'success');
};

const irParaInvestir = () => {
  router.push('/investir');
};

const atualizarGrafico = async () => {
  try {
    console.log('Atualizando gráfico...');

    // Aguarda o próximo ciclo de renderização
    await nextTick();

    if (!chartRef.value) {
      console.warn('Canvas não encontrado');
      return;
    }

    // Destrói a instância anterior do gráfico se existir
    if (chartInstance.value) {
      chartInstance.value.destroy();
      chartInstance.value = null;
    }

    const ctx = chartRef.value.getContext('2d');
    if (!ctx) {
      console.error('Não foi possível obter o contexto 2D do canvas');
      return;
    }

    // Configura o container do gráfico
    const chartContainer = chartRef.value.parentElement;
    chartContainer.style.position = 'relative';

    // Remove qualquer texto central existente para evitar sobreposição
    const existingText = chartContainer.querySelector('.chart-center-text');
    if (existingText) {
      existingText.remove();
    }

    // Cria o elemento de texto central
    const centerText = document.createElement('div');
    centerText.className = 'chart-center-text';
    centerText.style.position = 'absolute';
    centerText.style.top = '50%';
    centerText.style.left = '50%';
    centerText.style.transform = 'translate(-50%, -50%)';
    centerText.style.fontSize = '24px';
    centerText.style.fontWeight = 'bold';
    centerText.style.color = '#FFFFFF';
    centerText.style.textAlign = 'center';
    centerText.style.pointerEvents = 'none';
    centerText.textContent = '100%';

    // Adiciona o texto ao container do gráfico
    chartContainer.appendChild(centerText);

    // Prepara os dados do gráfico
    const labels = [];
    const data = [];
    const colors = [];

    carteira.value.forEach((item, index) => {
      if (item.porcentagem > 0) {
        labels.push(item.nome);
        data.push(item.porcentagem);
        colors.push(coresGrafico[index % coresGrafico.length]);
      }
    });

    console.log('Dados do gráfico:', { labels, data, colors });

    // Cria o gráfico
    chartInstance.value = new Chart(ctx, {
      type: 'doughnut',
      data: {
        labels: labels,
        datasets: [{
          data: data,
          backgroundColor: colors,
          borderWidth: 0,
          borderRadius: 8,
          spacing: 2,
          hoverOffset: 0,
          hoverBorderWidth: 0
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        cutout: '65%',
        radius: '100%',
        layout: {
          padding: 5
        },
        plugins: {
          legend: {
            display: false
          },
          tooltip: {
            enabled: false
          }
        },
        animation: {
          animateScale: true,
          animateRotate: true,
          duration: 500,
          easing: 'easeOutQuart'
        },
        elements: {
          arc: {
            borderWidth: 0,
            hoverBorderWidth: 0,
            hoverOffset: 0
          }
        },
        onClick: (event, elements) => {
          if (elements.length > 0) {
            const index = elements[0].index;
            const estrategia = carteira.value[index];
            if (estrategia) {
              // Atualiza o texto central com a porcentagem da fatia clicada
              const centerTextElement = chartContainer.querySelector('.chart-center-text');
              if (centerTextElement) {
                centerTextElement.textContent = `${estrategia.porcentagem}%`;
              }
            }
          } else {
            // Quando clica fora das fatias, restaura para 100%
            const centerTextElement = chartContainer.querySelector('.chart-center-text');
            if (centerTextElement) {
              centerTextElement.textContent = '100%';
            }
          }
        }
      }
    });

    console.log('Gráfico criado com sucesso');
  } catch (error) {
    console.error('Erro ao criar gráfico:', error);
  }
};

const carregarCarteira = async () => {
  try {
    if (!carregando.value) {
      carregando.value = true;
    }

    console.log('Carregando carteira...');
    const response = await api.get('/carteira');
    console.log('Dados recebidos da API:', response.data);

    // Sempre atualiza a carteira com os dados mais recentes
    const dadosAtualizados = response.data.map(item => ({
      ...item,
      aberto: false, // Fecha todos os itens por padrão
      ativos: (item.ativos || []).map(ativo => ({
        ...ativo,
        quantidadeVenda: 0,
        precoVenda: ativo.valor_medio || ativo.preco_atual || 0,
        // Garante que temos o código do ativo disponível
        codigo: ativo.codigo || ativo.codigo_ativo
      }))
    }));

    carteira.value = dadosAtualizados;

    // Força a atualização do gráfico após carregar os dados
    await nextTick();
    if (dadosAtualizados.length > 0) {
      atualizarGrafico();
    }

    console.log('Carteira carregada:', dadosAtualizados);
    carregando.value = false;
  } catch (error) {
    console.error('Erro ao carregar carteira:', error);
    mostrarMensagem('Erro ao carregar carteira', 'danger');
    carregando.value = false;
  }
};

const mostrarMensagem = async (mensagem, cor, persistente = false) => {
  const toast = await toastController.create({
    message: mensagem,
    duration: persistente ? 0 : 3000,
    color: cor,
    position: 'top',
    buttons: persistente ? [] : [{ icon: 'close' }]
  });
  await toast.present();
  return toast;
};

const configurarCarrossel = () => {
  nextTick(() => {
    const carousel = document.querySelector('.legend-container');
    if (carousel) {
      const itemWidth = 200;
      const totalWidth = legendasDuplicadas.value.length * itemWidth / 3;
      carousel.style.width = `${totalWidth}px`;
    }
  });
};

const pausarCarrossel = () => {
  carrosselPausado.value = true;
};

const retomarCarrossel = () => {
  carrosselPausado.value = false;
};

const toqueInicio = (event) => {
  touchStartX = event.touches[0].clientX;
};

const toqueFim = (event) => {
  touchEndX = event.changedTouches[0].clientX;
  const diffX = touchStartX - touchEndX;
  if (Math.abs(diffX) > 50) {
    // Swipe left or right - could add logic to move carousel
  }
};

const configurarEventListeners = () => {
  window.addEventListener('carteira-atualizada', carregarCarteira);

  router.beforeEach((to, from, next) => {
    if (to.path === '/carteira' && from.path !== '/carteira') {
      nextTick(() => carregarCarteira());
    }
    next();
  });
};

onMounted(() => {
  carregarCarteira();
  configurarCarrossel();
  configurarEventListeners();
});

onBeforeUnmount(() => {
  if (carrosselInterval) {
    clearInterval(carrosselInterval);
  }

  if (pollingInterval) {
    clearInterval(pollingInterval);
  }

  if (chartInstance.value) {
    chartInstance.value.destroy();
  }

  window.removeEventListener('carteira-atualizada', carregarCarteira);
});

watch(carteira, (newCarteira) => {
  if (newCarteira.length > 0) {
    legendasDuplicadas.value = [...newCarteira, ...newCarteira, ...newCarteira];
    nextTick(() => {
      atualizarGrafico();
    });
  }
}, { deep: true });
</script>

<style lang="scss">
@import '@/theme/carteira.scss';
</style>
