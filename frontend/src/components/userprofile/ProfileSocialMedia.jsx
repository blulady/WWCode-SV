import React from "react";

import ProfileSection from "./ProfileSection";
import TextField from "./forms/TextField";

export const ProfileSocialMedia = ({ slack_handle, linkedin, instagram, facebook, twitter, medium, readonly, onChange }) => {
    return (
            <ProfileSection header="Social Media">
                <TextField id="slackField" label="Slack Handle" type="text" name="slack_handle" value={slack_handle} readonly={readonly} onChange={onChange}></TextField>
                <TextField id="linkedinField" label="LinkedIn" type="text" name="linkedin" value={linkedin} readonly={readonly} onChange={onChange}></TextField>
                <TextField id="instagramField" label="Instagram" type="text" name="instagram" value={instagram} readonly={readonly} onChange={onChange}></TextField>
                <TextField id="facebookField" label="Facebook" type="text" name="facebook" value={facebook} readonly={readonly} onChange={onChange}></TextField>
                <TextField id="twitterField" label="Twitter" type="text" name="twitter" value={twitter} readonly={readonly} onChange={onChange}></TextField>
                <TextField id="mediumField" label="Medium" type="text" name="medium" value={medium} readonly={readonly} onChange={onChange}></TextField>
            </ProfileSection>
    );
};

export default ProfileSocialMedia;