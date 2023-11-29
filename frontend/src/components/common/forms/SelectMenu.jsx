import React from "react";
import cx from "classnames";
import FormLabelField from "./FormLabelField";

const SelectMenu = ({ id, label, options, value, onChange, name="", readonly=false, required=false }) => {
    return (
        <FormLabelField id={id} label={label} readonly={readonly} required={required}>
            <select id={id} name={name} className={cx({ "form-control": !readonly, "form-control-plaintext disabled": readonly })} onChange={onChange} value={value} readOnly={readonly}>
                {options.map((option, index) => {
                    return <option value={option.value} key={id + "_option_" + index}>{option.label}</option>
                })}
            </select>
        </FormLabelField>
    );
};

export default SelectMenu;