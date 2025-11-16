<template>
  <ion-page class="profile-page">
    <ion-content class="h-screen overflow-hidden" :scroll-y="false">
      <div class="profile-container">
        <div class="profile-box">
          <div class="logo-wrapper">
            <img
              src="@/assets/imagem/logo.png"
              alt="GrowGuru"
            />
          </div>
          <div class="title-section">
            <h1 class="profile-title">Editar Perfil</h1>
          </div>

          <form @submit.prevent="handleUpdateProfile" class="profile-form">
            <!-- Nome -->
            <div class="form-group">
              <label>Nome</label>
              <div class="input-wrapper">
                <ion-input
                  v-model="nome"
                  type="text"
                  placeholder="Digite seu nome"
                  required
                ></ion-input>
              </div>
            </div>

            <!-- Nova Senha -->
            <div class="form-group">
              <label>Nova Senha (opcional)</label>
              <div class="input-wrapper">
                <ion-input
                  v-model="novaSenha"
                  :type="showNewPassword ? 'text' : 'password'"
                  placeholder="Digite a nova senha"
                ></ion-input>
                <div
                  @click="showNewPassword = !showNewPassword"
                  class="toggle-password"
                >
                  <ion-icon
                    :icon="showNewPassword ? eyeOffOutline : eyeOutline"
                  ></ion-icon>
                </div>
              </div>
            </div>

            <!-- Confirmar Nova Senha -->
            <div class="form-group">
              <label>Confirmar Nova Senha</label>
              <div class="input-wrapper">
                <ion-input
                  v-model="confirmarNovaSenha"
                  :type="showConfirmNewPassword ? 'text' : 'password'"
                  placeholder="Confirme a nova senha"
                ></ion-input>
                <div
                  @click="showConfirmNewPassword = !showConfirmNewPassword"
                  class="toggle-password"
                >
                  <ion-icon
                    :icon="showConfirmNewPassword ? eyeOffOutline : eyeOutline"
                  ></ion-icon>
                </div>
              </div>
            </div>

            <!-- Botão de Atualizar -->
            <button
              type="submit"
              class="submit-button"
              :disabled="loading"
            >
              <ion-spinner
                v-if="loading"
                name="crescent"
              ></ion-spinner>
              <span>{{ loading ? 'Atualizando...' : 'Atualizar Perfil' }}</span>
            </button>

            <!-- Botão Voltar -->
            <button
              type="button"
              @click="goBack"
              class="back-button-outline"
            >
              <ion-icon :icon="arrowBackOutline"></ion-icon>
              <span>Voltar</span>
            </button>
          </form>
        </div>
      </div>
    </ion-content>
  </ion-page>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { api } from '@/api';
import { eyeOutline, eyeOffOutline, arrowBackOutline } from 'ionicons/icons';
import {
  IonPage,
  IonContent,
  IonInput,
  IonIcon,
  IonSpinner,
  toastController
} from '@ionic/vue';

const showNewPassword = ref(false);
const showConfirmNewPassword = ref(false);

const router = useRouter();
const nome = ref('');
const novaSenha = ref('');
const confirmarNovaSenha = ref('');

const loading = ref(false);

const showToast = async (message, color = 'success') => {
  const toast = await toastController.create({
    message,
    duration: 3000,
    color,
    position: 'top'
  });
  await toast.present();
};

const goBack = () => {
  router.push('/tabs/home');
};

const handleUpdateProfile = async () => {
    try {
      loading.value = true;

      // Validação do nome
      if (!nome.value || nome.value.trim() === '') {
        await showToast('Por favor, insira seu nome.', 'warning');
        loading.value = false;
        return;
      }

      // Validação de senha
      if (novaSenha.value || confirmarNovaSenha.value) {
        if (!novaSenha.value) {
          await showToast('Por favor, insira a nova senha.', 'warning');
          loading.value = false;
          return;
        }
        
        if (novaSenha.value !== confirmarNovaSenha.value) {
          await showToast('As senhas não coincidem.', 'warning');
          loading.value = false;
          return;
        }
        
        if (novaSenha.value.length < 6) {
          await showToast('A senha deve ter pelo menos 6 caracteres.', 'warning');
          loading.value = false;
          return;
        }
      }

      // Preparar os dados para envio
      const payload = {
        nome: nome.value.trim(),
      };

      // Adicionar a senha apenas se fornecida
      if (novaSenha.value) {
        payload.novaSenha = novaSenha.value;
      }

      console.log('Enviando requisição para atualizar perfil...');
      
      // Fazer a requisição para a API
      const response = await api.put('/profile', payload);
      
      // Verificar se a resposta foi bem-sucedida
      if (response.data && response.data.success) {
        // Se a atualização for bem-sucedida, atualizar os dados locais
        if (response.data.user) {
          // Atualizar o nome exibido se retornado pelo servidor
          nome.value = response.data.user.nome || nome.value;
        }
        
        // Mostrar mensagem de sucesso
        await showToast(response.data.message || 'Perfil atualizado com sucesso!');
        
        // Redirecionar para a tela inicial após 1 segundo
        setTimeout(() => {
          router.push('/tabs/home');
        }, 1000);
      } else {
        // Se a API retornar sucesso: false
        const errorMsg = response.data?.error || 'Erro ao atualizar perfil. Tente novamente.';
        await showToast(errorMsg, 'danger');
      }
      
    } catch (error) {
      console.error('Erro ao atualizar perfil:', error);
      
      // Tratamento de erros específicos
      let errorMessage = 'Erro ao atualizar perfil. Tente novamente.';
      
      if (error.response) {
        // Erro retornado pelo servidor
        const { data, status } = error.response;
        
        if (status === 401) {
          errorMessage = 'Sessão expirada. Por favor, faça login novamente.';
          // Redirecionar para a tela de login
          setTimeout(() => {
            router.push('/login');
          }, 2000);
        } else if (status === 400) {
          // Erros de validação do servidor
          errorMessage = data.error || 'Dados inválidos. Verifique as informações e tente novamente.';
        } else if (data && data.code === 'INVALID_PASSWORD') {
          errorMessage = 'A senha fornecida não atende aos requisitos mínimos.';
        } else if (data && data.code === 'DUPLICATE_USERNAME') {
          errorMessage = 'Este nome de usuário já está em uso. Escolha outro.';
        }
      } else if (error.request) {
        // A requisição foi feita mas não houve resposta
        errorMessage = 'Não foi possível conectar ao servidor. Verifique sua conexão com a internet.';
      }
      
      // Exibir mensagem de erro para o usuário
      await showToast(errorMessage, 'danger');
      
    } finally {
      loading.value = false;
    }
};

// Load current user data on mount
const loadUserData = async () => {
  try {
    const { data } = await api.get('/usuarios');
    nome.value = data.nome;
  } catch (error) {
    console.error('Erro ao carregar dados do usuário:', error);
  }
};

// Load data when component mounts
onMounted(() => {
  loadUserData();
});
</script>

<style lang="scss" scoped>
@import '@/theme/profile.scss';
</style>
