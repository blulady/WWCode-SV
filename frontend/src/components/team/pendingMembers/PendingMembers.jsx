import React from "react";
import { useEffect } from "react";
import { useState } from "react";
import { isBrowser } from "react-device-detect";
import { useNavigate } from "react-router-dom";
import WwcApi from "../../../WwcApi";
import PendingMemberList from "./PendingMemberList";
import PendingMemberTable from "./PendingMemberTable";
import ModalDialog from "../../common/ModalDialog";
import MessageBox from "../../messagebox/MessageBox";
import {
  ERROR_TEAM_MEMBERS_UNABLE_TO_LOAD,
  ERROR_REQUEST_MESSAGE,
} from "../../../Messages";
import styles from "./PendingMembers.module.css";

const PendingMembers = (props) => {
  const [users, setUsers] = useState([]);
  const [apiError, setApiError] = useState(null);
  const [showMessage, setShowMessage] = useState(false);
  const [currentUser, setCurrentUser] = useState(null);
  const navigate = useNavigate();

  const renderTable = () => {
    return (
      <PendingMemberTable
        users={users}
        target="#resendConfirmationDialog"
        targetDelete="#deletePendingMemberDialog"
        onDeleteMember={handelDeleteMember}
      />
    );
  };
  const renderList = () => {
    return (
      <PendingMemberList
        users={users}
        target="#resendConfirmationDialog"
        targetDelete="#deletePendingMemberDialog"
      ></PendingMemberList>
    );
  };

  const getInvitees = async () => {
    try {
      let _users = await WwcApi.getInvitees();
      setUsers(_users);
    } catch (error) {
      setApiError(ERROR_TEAM_MEMBERS_UNABLE_TO_LOAD.replace("{0}", ""));
      console.log(error);
    }
  };

  const goToAddMember = () => {
    navigate("/member/add");
  };

  const resendInvite = async () => {
    try {
      await WwcApi.resendInvite(currentUser);
      await getInvitees();
      setShowMessage(true);
    } catch (error) {
      setApiError(ERROR_REQUEST_MESSAGE);
      console.log(error);
    }
  };

  const handelDeleteMember = () => {
    const temp = [...users];
    const filteredMembers = temp.filter((member) => member.id !== +currentUser);
    setUsers(filteredMembers);
    WwcApi.deleteInvitees(currentUser).catch((err) => {
      setUsers(temp);
      setApiError(ERROR_REQUEST_MESSAGE);
    });
  };

  const onOpeningModalDialog = (target) => {
    if (target) {
      const user = target.getAttribute("data-bs-user");
      setCurrentUser(user);
    }
  };

  useEffect(() => {
    getInvitees();
  }, []);

  return (
    <div className={styles["pending-members-container"]}>
      <div className="d-flex justify-content-end mb-2 mb-md-5">
        <button
          type="button"
          className="wwc-action-button"
          onClick={goToAddMember}
        >
          + Add Member
        </button>
      </div>
      {showMessage && (
        <div className="d-flex justify-content-center">
          <MessageBox
            type="Success"
            title="Success!"
            message="New registration link has been sent."
          ></MessageBox>
        </div>
      )}
      {apiError && (
        <div className="d-flex justify-content-center">
          <MessageBox
            type="Error"
            title="Sorry!"
            message={apiError}
          ></MessageBox>
        </div>
      )}
      {users.length ? (
        isBrowser ? (
          renderTable()
        ) : (
          renderList()
        )
      ) : (
        <div className={styles["no-users-msg"]}>No invitees to display</div>
      )}
      <ModalDialog
        id="resendConfirmationDialog"
        title="Are you sure?"
        text="Are you sure you want to resend the registration link?"
        onConfirm={resendInvite}
        onOpening={onOpeningModalDialog}
        onCancel={() => {}}
      ></ModalDialog>
      <ModalDialog
        id="deletePendingMemberDialog"
        title="Are you sure?"
        text="Are you sure you want to permanently delete this invitee from the records?"
        onConfirm={handelDeleteMember}
        onOpening={onOpeningModalDialog}
        onCancel={() => {}}
      ></ModalDialog>
    </div>
  );
};

export default PendingMembers;
