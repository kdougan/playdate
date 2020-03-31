<template>
  <div class="auth">
    <div class="login-screen">
      <div class="app-title">
        <h1>Login</h1>
      </div>

      <div class="login-form">
        <div class="control-group">
          <input
            type="text"
            class="login-field"
            v-model="username"
            placeholder="username"
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
      </div>
    </div>
  </div>
</template>

<script>
import authService from '../service/auth';
export default {
  data: () => ({
    username: '',
    password: ''
  }),
  methods: {
    submit(e) {
      e.preventDefault();
      console.log('Auth:submit', this);
      authService.login(this.username, this.password);
    }
  }
};
</script>

<style lang="scss" scoped>
.auth {
  margin: 20px auto;
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