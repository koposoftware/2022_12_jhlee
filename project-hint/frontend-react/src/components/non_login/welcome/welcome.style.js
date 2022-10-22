import styled, { keyframes } from "styled-components";
import { slideInUp } from "react-animations";

const showUpAnimation = keyframes`${slideInUp}`;

export const TemplateBlock = styled.div`
  background: white;
  position: absolute;
  top: 0;
  left: 0;
  bottom: 0;
  right: 0;
  display: flex;
  flex-direction: center;
  justify-content: center;
  align-items: center;
  white-space: pre-wrap;
  background: #F7F7F7;
`;
export const DivideLine = styled.div`
  width: 135px;
  height: 3.5px;
  background: --hana-green;
  margin-top: 122px;
  margin-left: 171px;
  margin-bottom: 15px;
`;
export const Title = styled.div`
  font-size: 40px;
  font-family: NotoSansKR-T;
  color: black;
  margin-left: 171px;
`;
export const BoldTitle = styled.div`
  font-size: 40px;
  font-family: NotoSansKR-B;
  color: black;
  margin-left: 171px;
`;
const animation = keyframes`
  25% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.5);
  }
  100% {
    transform: scale(1.2);
  }
`;
export const BoldGreenTitle = styled.div`
  font-size: 90px;
  font-family: Baloo;
  color: var(--hana-green);
  margin-left: 201px;
  animation: ${animation} 2.5s forwards;
`;
export const Row = styled.div`
  display: flex;
  // background-color: #ffffff;
  background: #F7F7F7;
`;
export const Content = styled.div`
  font-size: 18.5px;
  color: black;
  font-family: NotoSansKR-L;
  width: 387px;
  margin-left: 171px;
`;
export const StartBtn = styled.button`
  width: 235px;
  height: 52px;
  background: white;

  box-shadow: 0px 3px 7px 0px rgba(0, 0, 0, 0.2);
  margin-top: 41px;
  border-radius: 25px;
  border-width: medium;
  margin-left: 171px;
  color: black;
  font-size: 18px;
  font-family: NotoSansKR-M;
  outline: none;

  cursor: pointer;

  &:hover {
    background-color: var(--hana-green);
    color: white;
  }
`;

export const Show1Div = styled.div`
  background-color: white;
  animation: 1s ${showUpAnimation};
  background: #F7F7F7;
`;

export const Show2Div = styled.div`
  background-color: white;
  animation: 1s ${showUpAnimation};
  background: #F7F7F7;
`;
