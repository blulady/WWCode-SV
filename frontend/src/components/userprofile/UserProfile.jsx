import React, { useState, useEffect } from "react";
import ContainerWithNav from "../layout/ContainerWithNav";

import Spinner from "../layout/Spinner";

import WwcApi from "../../WwcApi";

import styles from "./UserProfile.module.css"

import MessageBox from "../messagebox/MessageBox";
import { ERROR_REQUEST_MESSAGE, SUCCESS_USER_PROFILE } from "../../Messages";

import ViewProfile from "./ViewProfile";
import EditProfile from "./EditProfile";
import EditPassword from "./EditPassword";

export const UserProfile = () => {
  const [profileData, setProfileData] = useState({
    "id": "",
    "first_name": "",
    "last_name": "",
    "email": "",
    "status": "",
    "highest_role": "",
    "date_joined": "",
    "role_teams": [],
    "city": "",
    "state": "",
    "country": "",
    "timezone": "",
    "bio": "",
    "photo": "",
    "slack_handle": "",
    "linkedin": "",
    "instagram": "",
    "facebook": "",
    "twitter": "",
    "medium": ""
});

  const [message, setMessage] = useState({ show: false });

  // view, edit_profile, edit_password
  // initial mode is view
  const [mode, setMode] = useState("view");

  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const getMyMemberData = async () => {
      try {
        let myMembership = await WwcApi.getUserProfile();
        // normalize
        for (const prop in myMembership) {
          if (myMembership[prop] === null) {
            myMembership[prop] = "";
          }
        }
        setProfileData(myMembership);
      } catch (e) {
        setMessage({
          show: true,
          type: "Error",
          title: "Sorry!",
          content: ERROR_REQUEST_MESSAGE
        });
      } finally {
        setLoading(false);
      }
    };
    setLoading(true);
    getMyMemberData()
  }, [])


  const onClickEditProfile = () => {
    setEditMode("edit_profile");
  };

  const onClickEditPassword = () => {
    setEditMode("edit_password")
  };
  
  const setEditMode = (type) => {
    setMessage({ show: false });
    setMode(type);
  };

  const onSubmitEditForm = async (profile) => {
    const res = await WwcApi.editUserProfile(profile);
    if (res.status !== 200) {
      setMessage({ // Show error message and keep modal open
        show: true,
        type: "Error",
        title: "Sorry!",
        content: ERROR_REQUEST_MESSAGE
      });
    } else {
      setProfileData(profile);
      setMode("view");
      setMessage({ // Show success message
        show: true,
        type: "Success",
        title: "Success!",
        content: SUCCESS_USER_PROFILE
      });
    }
  };

  const onCancelEdit = (profile) => {
    setProfileData(profile);
    setMode("view")
  };

  // for password
  const onSubmitEditPassword = (result) => {
    if (result.status === "success") {
        setMessage({ // Show success message
          show: true,
          type:"Success",
          title: "Success!",
          content: SUCCESS_USER_PROFILE
        });
        setMode("view");
    } else {
      setMessage({ // Show error message and keep modal open
        show: true,
        type:"Error",
        title: "Sorry!",
        content: ERROR_REQUEST_MESSAGE
      });
    }
  };

  const renderMessageBox = () => {
    if (message.show) {
      return <MessageBox type={message.type} title={message.title} message={message.content}></MessageBox>
    } 
  };

  const renderUserProfile = () => {
    // Loading
    if (loading) {
      return (<div className="text-center">
        <Spinner />
      </div>)
    }

    switch (mode) {
      case "edit_password":
        return <EditPassword submit={onSubmitEditPassword} closeEditModal={() => setMode("view")}></EditPassword>;
      case "edit_profile":
        return <EditProfile profileData={profileData} onSubmitEditForm={onSubmitEditForm} onCancelEdit={onCancelEdit}></EditProfile>;
      default:
        return <ViewProfile profileData={profileData} onClickEditPassword={onClickEditPassword} onClickEditProfile={onClickEditProfile}></ViewProfile>;
    }
  };

  return (
    <ContainerWithNav>
      <div className={styles["p_container"]}>
        <div className={styles["p_inner_container"]}>
          {renderMessageBox()}
          {renderUserProfile()}
        </div>
      </div>

    </ContainerWithNav>
  )
}

export default UserProfile