import React from "react";

import ModalConfirm from "../../common/ModalConfirm";
import styles from "./PendingMemberTable.module.css";

const TableBody = ({ users, target, onDeleteMember }) => {
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
            <button
              className={styles["invite-button"]}
              type="button"
              data-bs-toggle="modal"
              data-bs-target={target}
              data-bs-user={user.id}
            >
              Resend Invite
            </button>
          </td>
          <td>
            <ModalConfirm
              title={"Are you sue?"}
              description={
                "Are you sure you want to permanently delete this invitee from the records?"
              }
              onConfirm={() => onDeleteMember(user.id)}
              okText="OK"
            >
              <button
                className={styles["delete"] + " " + styles["icon"]}
              ></button>
            </ModalConfirm>
          </td>
        </tr>
      ))}
    </tbody>
  );
};

export default TableBody;
