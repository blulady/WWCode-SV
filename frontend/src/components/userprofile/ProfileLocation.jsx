import React from "react";

import ProfileSection from "./ProfileSection";
import SelectMenu from "../common/forms/SelectMenu";
import TextField from "../common/forms/TextField";

import ct from "countries-and-timezones";

const countries = Object.values(ct.getAllCountries()).map((c) => ({ label: c.name, value: c.id }));

const timezones = Object.values(ct.getAllTimezones()).map((t) => ({ label: t.name, value: t.name.toLocaleLowerCase().replaceAll("/", "_") }));

export const ProfileLocation = ({ country, state, city, timezone, onChange, readonly }) => {
    return (
        <ProfileSection header="Location & Timezone">
            <SelectMenu id="p_country" label="Country" name="country" options={countries} value={country} readonly={readonly} onChange={onChange}></SelectMenu>
            <TextField id="p_state" label="State" type="text" name="state" readonly={readonly} onChange={onChange} value={state || ""}></TextField>
            <TextField id="p_city" label="City" type="text" name="city" readonly={readonly} onChange={onChange} value={city || ""}></TextField>
            <SelectMenu id="c_timezone" label="Timezone" name="timezone" options={timezones} value={timezone} readonly={readonly} onChange={onChange}></SelectMenu>
        </ProfileSection>
    );
};

export default ProfileLocation;