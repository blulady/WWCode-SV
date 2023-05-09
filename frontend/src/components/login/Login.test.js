import React from 'react';
import { render } from '@testing-library/react';
import Login from './Login';
import AuthProvider from "../../context/auth/AuthProvider";
import Router from "react-router-dom";

const mockedUsedNavigate = jest.fn();

jest.mock('react-router-dom', () => ({
   ...jest.requireActual('react-router-dom'),
  useNavigate: () => mockedUsedNavigate,
  useSearchParams: jest.fn()
}));

it(' it should render  login form', () => {
  jest.spyOn(Router, "useSearchParams").mockReturnValue([new URLSearchParams({})]);
  const handleSetAuth = jest.fn();
  const {getByTestId ,getByText, findByLabelText} = render(
    <AuthProvider value={{handleSetAuth,}}> 
      <Login />
    </AuthProvider>
  );
  const loginForm = getByTestId("login-form");
  const submitBtn = getByTestId('login-submit-btn');
  const passwdInp = getByTestId('login-password');
  const emailInp = getByTestId('login-email');
 
  expect(getByText(/Email */i)).toBeTruthy();
  expect(getByText(/Chapter Tools Login/i)).toBeInTheDocument();
  expect(getByText(/Submit/i)).toBeTruthy();
  expect(findByLabelText(/Password */i)).toBeTruthy();
  expect(getByText(/SHOW/i)).toBeTruthy();
  expect(getByText(/Forgot your password?/i)).toBeTruthy();
  expect(loginForm).toBeInTheDocument();
  expect(emailInp).toBeInTheDocument();
  expect(emailInp).toHaveAttribute('required');
  expect(passwdInp).toBeInTheDocument();
  expect(passwdInp).toHaveAttribute('required');
  expect(submitBtn).toBeInTheDocument();
  expect(submitBtn).toHaveAttribute('disabled');
});

it('Login with register param', () => {
  jest.spyOn(Router, "useSearchParams").mockReturnValue([new URLSearchParams({ "register": true })]);
  const handleSetAuth = jest.fn();
  const {getByTestId ,getByText, findByLabelText} = render(
    <AuthProvider value={{handleSetAuth,}}> 
      <Login />
    </AuthProvider>
  );

  expect(getByText(/Registration Successful */i)).toBeTruthy();
});