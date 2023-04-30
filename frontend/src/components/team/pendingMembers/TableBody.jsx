import React, {useState} from 'react'

import PopupConfirm from '../../common/Popconfirm';
import styles from "./PendingMemberTable.module.css";

const TableBody = ({users, target}) => {
    const [members, setMembers] = useState(users);

    const handelDeleteMember = (userId) => {
        let temp = [...members];
        temp = temp.filter(member => member.id !== userId);
        setMembers(temp);
    }

    return (
        <tbody>{members.map((user, idx) => (
            <tr key={user.id}>
              <td>{idx + 1}</td>
              <td>{user.email}</td>
              <td className="wwc-text-capitalize">{user.role_name.toLowerCase()}</td>
              <td className="wwc-text-capitalize">{user.status.toLowerCase()}</td>
              <td>
                <button
                  className={styles["invite-button"]}
                  type="button"
                  data-bs-toggle="modal"
                  data-bs-target={target}
                  data-bs-user={user.email}
                >
                  Resend Invite
                </button>
              </td>
              <td>
                <PopupConfirm
                  title={"Are you sue?"}
                  description={
                    "Are you sure you want to permanently delete this invitee from the records?"
                  }
                  onConfirm={() => handelDeleteMember(user.id)}
                  onCancel={() => console.log("cancel")}
                >
                  <button className={styles["delete"] + " " + styles["icon"]}></button>
                </PopupConfirm>
              </td>
            </tr>
          ))}
        </tbody>
    )
}

export default TableBody;