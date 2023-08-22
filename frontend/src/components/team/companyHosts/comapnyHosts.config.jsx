import React from "react";
import WwcApi from "../../../WwcApi";
import Dropdown from "../../common/Dropdown";
import TruncatedText from "../companyHosts/TruncatedText";
import ModalDialog from "../../common/ModalDialog";
import styles from "./CompanyHosts.index.module.css";
import Contacts from "./Contacts";

export const columns = [
  {
    key: "id",
    title: "",
    dataIndex: "id",
  },
  {
    key: "company",
    title: "Company",
    dataIndex: "company",
  },
  {
    key: "city",
    title: "City",
    dataIndex: "city",
  },
  {
    key: "contacts",
    title: "Contacts",
    dataIndex: "contacts",
    render: (data) => {
      return <Contacts data={data}/>
    },
  },
  {
    key: "notes",
    title: "Notes",
    dataIndex: "notes",
    render: (notes) => {
      return <TruncatedText text={notes} />;
    },
  },
  {
    key: "actions",
    title: "Actions",
    dataIndex: "",
    render: (_, record) => {
      const handleDeleteCompanyHost = (companyId) => {
        WwcApi.deleteCompanyHost(companyId).catch((err) => {
          console.log(err);
        });
      };
      return (
        <ModalDialog
          id="deleteCompanyHost"
          title="Are you sure?"
          text="Are you sure you want to delete the company host?"
          onConfirm={() => handleDeleteCompanyHost(record.id)}
        >
          <button
            className={styles["delete"] + " " + styles["icon"]}
            type="button"
          />
        </ModalDialog>
      );
    },
  },
];
