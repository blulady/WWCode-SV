import React, { useState, useEffect } from "react";
import GenericTable from "../../common/Table";
import WwcApi from '../../../WwcApi'
import styles from "./CompanyHosts.index.module.css";
import TruncatedText from "./TruncatedText";
import ModalDialog from "../../common/ModalDialog";
import Contacts from "./Contacts";


const CompanyHosts = () => {
  const [companyHosts, setCompanyHosts] = useState([]);
  const [currentRecord, setCurrentRecord] = useState(null);

  useEffect(() => {
    const fetchCompanyHost = async () => {
      try {
        const hosts = await WwcApi.getCompanyHost();
        setCompanyHosts(hosts.data);
      } catch (error) {
        console.log("An error occurred while fetching company hosts:", error);
      }
    }
    fetchCompanyHost();
  }, []);

  const handleDeleteCompanyHost = () => {
    WwcApi.deleteCompanyHost(currentRecord.id)
      .then((res) => {
        console.info(res.data.result);
        setCompanyHosts(companyHosts.filter((record) => record.id !== currentRecord.id));
        setCurrentRecord(null);
      })
      .catch((err) => {
        console.warn("Host deletion did not process.");
      });
  };

  const columns = [
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
        return <Contacts data={data} />
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
        return (
          <ModalDialog
            id="deleteCompanyHost"
            title="Are you sure?"
            text="Are you sure you want to delete the company host?"
            onConfirm={handleDeleteCompanyHost}
            onCancel={() => setCurrentRecord(null)}
          >
            <button
              className={styles["delete"] + " " + styles["icon"]}
              type="button"
              onClick={(e) => {
                setCurrentRecord({ ...record });
                e.stopPropagation();
              }}
            />
          </ModalDialog>
        );
      },
    },
  ];

  return (
    <GenericTable tableClass={styles["company-hosts-table"]} columns={columns} data={companyHosts} />
  );
};

export default CompanyHosts;
