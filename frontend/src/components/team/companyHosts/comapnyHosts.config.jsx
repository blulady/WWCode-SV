import React from "react";
import TruncatedText from "../companyHosts/TruncatedText";
import styles from "./CompanyHosts.index.module.css";

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
    render: (data, record) => {
      console.log(record);
      return data.map((item, index) => {
        return (
          <div key={index}>
            {item.name}_{item.email}
          </div>
        );
      });
    },
  },
  {
    key: "notes",
    title: "Notes",
    dataIndex: "notes",
    render: (notes) => {
        return <TruncatedText text={notes} />;
    }
  },
  {
    key: "actions",
    title: "Actions",
    dataIndex: "",
    render: () => {
      return (
        <button
          className={styles["delete"] + " " + styles["icon"]}
          type="button"
          data-bs-toggle="modal"
          //   data-bs-target={targetDelete}
          //   data-bs-user={user.id}
        />
      );
    },
  },
];
