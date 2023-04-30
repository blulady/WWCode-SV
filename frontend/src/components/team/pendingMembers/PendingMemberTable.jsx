import React from "react";

import WwcApi from "../../../WwcApi";
import TableBody from "./TableBody";
import styles from "./PendingMemberTable.module.css";

const PendingMemberTable = (props) => {

  return (
    <table className={styles["pending-members-table"]}>
      <thead>
        <tr>
          <th></th>
          <th>Email</th>
          <th>Role</th>
          <th>Status</th>
          <th>Resend Invite</th>
          <th>Actions</th>
        </tr>
      </thead>
      <TableBody users={props.users} target={props.target}/>
    </table>
  );
};

export default PendingMemberTable;
