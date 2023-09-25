import React, { useState } from "react";
import styles from "./Register.module.css";
import cx from 'classnames';
import { useSearchParams } from "react-router-dom";
import Spinner from "../layout/Spinner";
import WwcApi from "../../WwcApi";

import MessageBox from "../messagebox/MessageBox";
import { ERROR_REQUEST_MESSAGE, ERROR_REGISTER_LINK_INVALID, SUCCESS_REQUEST_REGISTER } from "../../Messages";
import RegistrationForm from "./RegistrationForm";


function Register(props) {
  const [searchParams] = useSearchParams();
  const email = searchParams.get("email");
  const token = searchParams.get("token");
  const [messageInfo, setMessageInfo] = useState({});
  const [processing, setProcessing] = useState(true);

  React.useEffect(() => {
    (async function validate() {
      WwcApi.validateInvitation({ params: { email, token } }) // check valid invitation
        .then((res) => {
          setProcessing(false);
          if (res.data.detail.status !== "ACTIVE" && res.data.detail.status !== "VALID") {
            setMessageInfo({ type: "Error", title: "Sorry!", message: ERROR_REGISTER_LINK_INVALID, showRequest: true });
          }
        })
        .catch((error) => {
          setMessageInfo({ type: "Error", title: "Sorry!", message: ERROR_REQUEST_MESSAGE }); // generic error
          setProcessing(false);
        });
    }());
  }, []); // only run once

  const resendLink = async () => {
    try {
      await WwcApi.requestRegistraionLink(email);
      setMessageInfo({ type: "Success", hasRequested: true, showRequest: false, title: "Success!", message: SUCCESS_REQUEST_REGISTER });
    } catch (error) {
      setMessageInfo({ type: "Error", title: "Sorry!", message: ERROR_REQUEST_MESSAGE });
      console.log(error);
    }
  };

  const renderMessageBox = () => {
    return (<MessageBox type={messageInfo.type} title={messageInfo.title} message={messageInfo.message}>
      {messageInfo.showRequest &&
        <button
          type="button"
          id="resendLink"
          className={styles["action-button"]}
          onClick={resendLink}
        >
          Request Registration Link
        </button>
      }
    </MessageBox>);
  };

  const renderComponent = () => {
    if (processing) {
      return (<Spinner />);
    }

    if (messageInfo.type) {
      return renderMessageBox();
    }

    return <RegistrationForm email={email} token={token} setMessageInfo={setMessageInfo} setProcessing={setProcessing} />;
  };

  return (
    <div className={cx('container-fluid', styles['container'])}>
      <div className={styles['WwcLogo']}></div>
      <main className={styles['register-main']}>
        {renderComponent()}
      </main>
    </div>
  );
}
export default Register;
