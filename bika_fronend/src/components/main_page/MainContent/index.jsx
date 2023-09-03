import React, { useState }  from 'react';
import './index.css';

import FunctionBlock21 from '../../FunctionBlocks/ChartBlock21';
import FunctionBlock11 from '../../FunctionBlocks/ChartBlock11';
import ChartComponent from '../../FunctionMains/ChartComponent';

function MainContent() {
  // 例如，可以根据需要生成多个功能方块
  const [modalIsOpen, setModalIsOpen] = useState(false);
  const [currentModal, setCurrentModal] = useState("");
  const blocks = [
    { label: '功能2_11', name_modal: "modal1", componentType: "type21", onClick: () => setCurrentModal("modal1")},
    { label: '功能2_1', name_modal: "modal2", componentType: "type21", onClick: () => setCurrentModal("modal1")},
    { label: '功能1_1', name_modal: "modal3", componentType: "type11", onClick: () => setCurrentModal("modal1")}
    // { label: '功能2', onClick: () => history.push('/feature2') },
    // { label: '功能3', onClick: () => history.push('/feature3') },
    // ... 其他功能方块
  ];

  const closeModal = () => {
    setModalIsOpen(false);
    setCurrentModal(null);
  }

  const renderModal = () => {
    switch (currentModal) {
      case "modal1":
        return <ChartComponent isOpen={modalIsOpen} onRequestClose={closeModal} />
      default:
        return null
    }
  }

  return (
    <div className="main-content">
      {blocks.map((bloc, index) => {
      switch (bloc.componentType) {
        case "type21":
          return <FunctionBlock21 key={index} {...bloc} />;
        case "type11":
          return <FunctionBlock11 key={index} {...bloc} />;
        default:
          return null; // 或者返回其他默认组件
      }
    })}
      {renderModal()}
    </div>
  );
}

export default MainContent;
