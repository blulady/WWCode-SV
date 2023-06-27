import React from "react";

import ModalDialog  from '../../common/ModalDialog'

import styles from "./PendingMemberTable.module.css";

const TableBody = ({ users, onResendInvite, onDeleteMember}) => {
  console.log(users)
  return (
    <tbody>
      {users.map((user, idx) => (
        <tr key={user.id}>
          <td>{idx + 1}</td>
          <td>{user.email}</td>
          <td className="wwc-text-capitalize">
            {user.role_name.toLowerCase()}
          </td>
          <td className="wwc-text-capitalize">{user.status.toLowerCase()}</td>
          <td>
          <ModalDialog
              id="resendConfirmationDialog"
              title="Are you sure?"
              text="Are you sure you want to resend the registration link?"
              onConfirm={() => onResendInvite(user.id)}
            >
            <button
              className={styles["invite-button"]}
              type="button"
            >
              Resend Invite
            </button>
            </ModalDialog>
          </td>
          <td>
            <ModalDialog
              id="deletePendingMemberDialog"
              title="Are you sure?"
              text="Are you sure you want to resend the registration link?"
              onConfirm={() => onDeleteMember(user.id)}
            >
              <button
                className={styles["delete"] + " " + styles["icon"]}
                type="button"
              />
            </ModalDialog>
          </td>
        </tr>
      ))}
    </tbody>
  );
};

export default TableBody;
