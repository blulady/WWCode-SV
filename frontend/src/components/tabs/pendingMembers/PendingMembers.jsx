import React from "react";
import { useEffect } from "react";
import { useState } from "react";
import { isBrowser } from "react-device-detect";
import { useNavigate } from "react-router-dom";
import WwcApi from "../../../WwcApi";
import PendingMemberList from "./PendingMemberList";
import PendingMemberTable from "./PendingMemberTable";
import MessageBox from "../../messagebox/MessageBox";
import {
  ERROR_TEAM_MEMBERS_UNABLE_TO_LOAD,
  ERROR_REQUEST_MESSAGE,
} from "../../../Messages";
import styles from "./PendingMembers.module.css";

const PendingMembers = () => {
  const [users, setUsers] = useState([]);
  const [apiError, setApiError] = useState(null);
  const [showMessage, setShowMessage] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    getInvitees();
  }, []);

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
        navigate("/member/add",{
            state: { pageId: "chapter", pending: true }
          });
    };

  const resendInvite = async (currentUser) => {
    try {
      await WwcApi.resendInvite(currentUser);
      await getInvitees();
      setShowMessage(true);
    } catch (error) {
      setApiError(ERROR_REQUEST_MESSAGE);
      console.log(error);
    }
  };

  const handleDeleteMember = async (currentUserId) => {
    const temp = [...users];
    try {
      await WwcApi.deleteInvitees(currentUserId)
      const filteredMembers = temp.filter(
        (member) => member.id !== currentUserId
      );
      setUsers(filteredMembers);
    } catch (err) {
      setUsers(temp);
      setApiError(ERROR_REQUEST_MESSAGE);
      console.error(err)
    }
  };

  const renderTable = () => {
    return (
      <PendingMemberTable
        users={users}
        onDeleteMember={handleDeleteMember}
        onResendInvite={resendInvite}
      />
    );
  };
  const renderList = () => {
    return (
      <PendingMemberList
        users={users}
        onResendInvite={resendInvite}
        onDeleteMember={handleDeleteMember}
      ></PendingMemberList>
    );
  };

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
    </div>
  );
};

export default PendingMembers;
