import React from "react";
import { render, screen, act, fireEvent } from "@testing-library/react";
import ConfirmResetPassword from "./ResetPasswordForm";
import AuthProvider from "../../context/auth/AuthProvider";

const mockNavigation = jest.fn();

jest.mock("../../WwcApi");

jest.mock('react-router-dom', () => {
  const ActualReactRouterDom = jest.requireActual('react-router-dom');
  return {
      ...ActualReactRouterDom,
      useNavigate: () => mockNavigation,
      useLocation: () => (
        {search: "?email=a@b.com&token=test"}
      )
  }
});

test('it should render reset password form', () => {
  const handleSetAuth = jest.fn();
  const { getByTestId } = render (
    <AuthProvider value={{handleSetAuth,}}> 
      <ConfirmResetPassword/>
    </AuthProvider>
  )

  const resetPwForm = getByTestId("reset-pw-form")
  const resetPwBtn = getByTestId("reset-pw-button")

  expect(resetPwForm).toBeInTheDocument();  
  expect(resetPwBtn).toBeInTheDocument(); 
});