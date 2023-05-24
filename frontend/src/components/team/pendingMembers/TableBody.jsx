import React from "react";

import styles from "./PendingMemberTable.module.css";

const TableBody = ({ users, target, targetDelete }) => {
  
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
            <button
              className={styles["delete"] + " " + styles["icon"]}
              type="button"
              data-bs-toggle="modal"
              data-bs-target={targetDelete}
              data-bs-user={user.id}
            />
          </td>
        </tr>
      ))}
    </tbody>
  );
};

export default TableBody;
