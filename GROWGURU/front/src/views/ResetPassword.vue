<template>
  <ion-page class="reset-password-page">
    <ion-content class="h-screen overflow-hidden" :scroll-y="false">
      <div class="reset-password-container">
        <div class="reset-password-box">
          <div class="logo-wrapper">
            <img src="@/assets/imagem/logo.png" alt="GrowGuru" />
          </div>
          <h1 class="title">Redefinir Senha</h1>

          <div class="reset-password-form">
            <div class="form-group">
              <label>Nova Senha</label>
              <div class="input-wrapper">
                <ion-input 
                  v-model="password" 
                  :type="showPassword ? 'text' : 'password'" 
                  placeholder="Digite sua nova senha" 
                  required>
                </ion-input>
                <IonIcon 
                  :icon="showPassword ? eyeOff : eye" 
                  class="password-toggle" 
                  @click="showPassword = !showPassword"
                  :aria-label="showPassword ? 'Ocultar senha' : 'Mostrar senha'"
                ></IonIcon>
              </div>
            </div>

            <div class="form-group">
              <label>Confirme a Nova Senha</label>
              <div class="input-wrapper">
                <ion-input 
                  v-model="confirmPassword" 
                  :type="showConfirmPassword ? 'text' : 'password'" 
                  placeholder="Confirme sua nova senha"
                  required>
                </ion-input>
                <IonIcon 
                  :icon="showConfirmPassword ? eyeOff : eye" 
                  class="password-toggle" 
                  @click="showConfirmPassword = !showConfirmPassword"
                  :aria-label="showConfirmPassword ? 'Ocultar confirmação de senha' : 'Mostrar confirmação de senha'"
                ></IonIcon>
              </div>
            </div>

            <div class="form-group">
              <div class="password-requirements">
                A senha deve conter pelo menos 8 caracteres, incluindo letras maiúsculas, minúsculas, números e
                caracteres especiais.
              </div>
            </div>

            <ion-button type="submit" expand="block" class="submit-button" :disabled="!isFormValid || isLoading">
              <ion-spinner v-if="isLoading" name="crescent" class="w-5 h-5"></ion-spinner>
              <span v-else>Redefinir Senha</span>
            </ion-button>
            <div class="login-container">
              <p>
                Lembrou sua senha?
                <router-link to="/login" class="login-link">Faça login</router-link>
              </p>
            </div>
            <div v-if="errorMessage" class="rp-message rp-message--error">{{ errorMessage }}</div>
            <div v-if="successMessage" class="rp-message rp-message--success">{{ successMessage }}</div>
          </div>


        </div>
      </div>
    </ion-content>
  </ion-page>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { warning, checkmarkCircle, eye, eyeOff } from 'ionicons/icons';
import { useRoute, useRouter } from 'vue-router';
import {
  IonPage,
  IonContent,
  IonInput,
  IonSpinner,
  IonButton,
  IonIcon,
  toastController,
  loadingController
} from '@ionic/vue';
import { supabase } from '@/lib/supabase'; // Certifique-se de que este caminho está correto

const route = useRoute();
const router = useRouter();
const password = ref('');
const confirmPassword = ref('');
const errorMessage = ref('');
const successMessage = ref('');
const isLoading = ref(false);
const showPassword = ref(false);
const showConfirmPassword = ref(false);
const token = ref('');

// Verifica o token de recuperação na URL
onMounted(async () => {
  const hash = window.location.hash.substring(1);
  const params = new URLSearchParams(hash);

  // O Supabase envia o token como access_token no hash
  const accessToken = params.get('access_token');
  const type = params.get('type');

  console.log('Token de acesso:', accessToken);
  console.log('Tipo de token:', type);

  if (accessToken && type === 'recovery') {
    token.value = accessToken;

    try {
      // Verifica o token de recuperação
      const { error } = await supabase.auth.verifyOtp({
        type: 'recovery',
        token_hash: accessToken,
      });

      if (error) {
        console.error('Erro ao verificar token:', error);
        // Não mostramos mensagem de erro aqui para permitir que o usuário tente redefinir
        // A validação final será feita no momento do envio
      } else {
        console.log('Token verificado com sucesso!');
      }
    } catch (err) {
      console.error('Erro ao verificar token:', err);
      // Não bloqueia o usuário, apenas registra o erro
    }
  } else if (!accessToken) {
    errorMessage.value = 'Link de redefinição inválido. Por favor, use o link completo enviado para o seu email.';
  }
});

// Verifica se o formulário é válido
const isFormValid = computed(() => {
  return (
    password.value.length >= 6 &&
    password.value === confirmPassword.value &&
    token.value
  );
});

const handleSubmit = async () => {
  if (password.value !== confirmPassword.value) {
    errorMessage.value = 'As senhas não coincidem.';
    return;
  }

  if (password.value.length < 6) {
    errorMessage.value = 'A senha deve ter pelo menos 6 caracteres.';
    return;
  }

  if (!token.value) {
    errorMessage.value = 'Token de redefinição não encontrado. Por favor, use o link completo enviado para o seu email.';
    return;
  }

  isLoading.value = true;
  errorMessage.value = '';
  successMessage.value = '';

  const loading = await loadingController.create({
    message: 'Redefinindo senha...',
    duration: 0
  });
  await loading.present();

  try {
    console.log('Atualizando senha...');

    // Atualiza a senha usando o Supabase
    const { data, error } = await supabase.auth.updateUser({
      password: password.value
    });

    if (error) throw error;

    console.log('Senha atualizada com sucesso:', data);
    successMessage.value = 'Senha redefinida com sucesso! Redirecionando para o login...';

    // Mostra mensagem de sucesso
    const toast = await toastController.create({
      message: 'Senha redefinida com sucesso!',
      duration: 3000,
      position: 'bottom',
      color: 'success'
    });
    await toast.present();

    // Redireciona para a página de login após 3 segundos
    setTimeout(() => {
      router.push('/login');
    }, 3000);

  } catch (error) {
    console.error('Erro ao redefinir senha:', error);

    let errorMessageText = 'Erro ao redefinir senha. Tente novamente.';

    if (error.message) {
      // Erro do Supabase
      console.error('Erro do Supabase:', error.message);

      if (error.message.includes('token') || error.message.includes('expired') || error.message.includes('invalid')) {
        errorMessageText = 'O link de redefinição é inválido ou expirou. Por favor, solicite um novo link de redefinição de senha.';
      } else {
        errorMessageText = 'Ocorreu um erro ao processar sua solicitação. Por favor, tente novamente ou tente outra senha.';
      }
    } else if (error.request) {
      // A requisição foi feita mas não houve resposta
      console.error('Sem resposta do servidor:', error.request);
      errorMessageText = 'Não foi possível conectar ao servidor. Verifique sua conexão.';
    } else {
      // Algo aconteceu na configuração da requisição
      console.error('Erro ao configurar a requisição:', error.message);
    }

    errorMessage.value = errorMessageText;

    // Mostra toast de erro
    const toast = await toastController.create({
      message: errorMessageText,
      duration: 3000,
      color: 'danger'
    });
    await toast.present();

  } finally {
    await loading.dismiss();
    isLoading.value = false;
  }
};
</script>

<style lang="scss" scoped>
@import '@/theme/reset-password.scss';

.rp-message {
  width: 100% !important;
  margin: 0.75rem 0 !important;
  padding: 0.75rem 1rem !important;
  border-radius: 0.5rem !important;
  font-size: 0.875rem !important;
  line-height: 1.5 !important;
  text-align: center !important;
  display: block !important;
  box-sizing: border-box !important;

  &--error {
    background-color: rgba(239, 68, 68, 0.1) !important;
    color: #ff0000 !important;
    font-weight: 500 !important;
    border: 1px solid rgba(239, 68, 68, 0.3) !important;
  }

  &--success {
    background-color: rgba(16, 185, 129, 0.1) !important;
    color: #008000 !important;
    font-weight: 500 !important;
    border: 1px solid rgba(16, 185, 129, 0.3) !important;
  }
}
</style>