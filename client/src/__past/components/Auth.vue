<template>
  <div class="auth">
    <b-container class="login-container" fluid>
      <div class="login-screen">
        <div class="app-title">
          <h1>Login</h1>
        </div>

        <form class="login-form" @submit="submit">
          <div class="control-group">
            <input
              type="text"
              class="login-field"
              v-model="email"
              placeholder="email"
              id="login-name"
            />
            <label class="login-field-icon fui-user" for="login-name"></label>
          </div>

          <div class="control-group">
            <input
              type="password"
              class="login-field"
              v-model="password"
              placeholder="password"
              id="login-pass"
            />
            <label class="login-field-icon fui-lock" for="login-pass"></label>
          </div>

          <a class="btn btn-primary btn-large btn-block" @click="submit">login</a>
          <a class="login-link" href="#">Lost your password?</a>
        </form>
      </div>
    </b-container>
  </div>
</template>

<script>
import { mapActions } from 'vuex';

export default {
  data: () => ({
    email: '',
    password: ''
  }),
  methods: {
    ...mapActions(['login', 'checkAuth']),
    submit(e) {
      e.preventDefault();
      this.login({ email: this.email, password: this.password });
    }
  }
};
</script>

<style lang="scss" scoped>
.auth {
  width: 100%;
}

.login-container {
  margin: 4rem auto;
  padding: 0;
  width: 300px;
}

.login-screen {
  background-color: #fff;
  padding: 20px;
  border-radius: 5px;
}

.app-title {
  text-align: center;
  color: #777;
}

.login-form {
  text-align: center;
}
.control-group {
  margin-bottom: 10px;
}

input {
  text-align: center;
  background-color: #ecf0f1;
  border: 2px solid transparent;
  border-radius: 3px;
  font-size: 16px;
  font-weight: 200;
  padding: 10px 0;
  width: 250px;
  transition: border 0.5s;
}

input:focus {
  border: 2px solid #3498db;
  box-shadow: none;
}

.btn {
  border: 2px solid transparent;
  background: #3498db;
  color: #ffffff;
  font-size: 16px;
  line-height: 25px;
  padding: 10px 0;
  text-decoration: none;
  text-shadow: none;
  border-radius: 3px;
  box-shadow: none;
  transition: 0.25s;
  display: block;
  width: 250px;
  margin: 0 auto;
  cursor: pointer;
}

.btn:hover {
  background-color: #2980b9;
}

.login-link {
  font-size: 12px;
  color: #444;
  display: block;
  margin-top: 12px;
}
</style>