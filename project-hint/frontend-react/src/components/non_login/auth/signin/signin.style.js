import styled, {keyframes} from "styled-components";
import {fadeIn} from "react-animations";

const fadeInAnimation = keyframes`${fadeIn}`;

export const SignInContainer = styled.div`
  margin: auto;
  // display: flex;
  position: relative;
  // top: -80px;
  bottom: 320px;
  // justify-content: center;
`;
export const SignInHeader = styled.div`
  font-size: 40px;
  font-family: NotoSansKR-M;
  display: flex;
  justify-content: center;
  margin-bottom: 50px;
  // background: #F7F7F7;
`;
export const LoginContainer = styled.div`
  margin: auto;
  // background: #F7F7F7;
`;
export const InputGroup = styled.div`
  margin-bottom: 25px;
  // background: #FFFFFF;
`;
export const Label = styled.div`
  font-size: 25px;
  margin-left: 11px;
  font-family: NotoSansKR-M, sans-serif;
  color: var(--brownish-grey);
`;

export const LoginInput = styled.input`
  // background: #F7F7F7;
  border: none;
  width: 400px;
  height: 40px;
  font-size: 15px;
  outline: none;
`;
export const InputBorder = styled.div`
  margin-top: 9px;
  width: 413px;
  height: 49px;

  border-radius: 18.8px;
  border: solid 1px var(--pinkish-grey);
  padding-left: 15px;
  align-items: center;

  display: flex;
  align-items: center;
  background: white;
`;

export const Checks = styled.div`
  margin-top: 8px;
  width: 413px;
  height: 12px;
  display: flex;
  justify-content: center;
`;

export const Check = styled.div`
  font-size: 12px;
  color: var(--brownish-grey);
  width: 120px;
  margin-left: 7px;
`;

export const Buttons = styled.div`
  display: flex;
  justify-content: space-around;
`;
export const ImgBtnContainer = styled.div`
  width: 430px;
  height: 45px;
  border: solid 1px var(--hana-green);
  border-radius: 18.8px;
  color: var(--greenish-teal);
  background-color: white;

  display: flex;
  justify-content: center;
  align-items: center;

  &:hover {
    background-color: var(--hana-green);
    color: white;
  }
`;

export const Img = styled.img`
  width: 18px;
  height: 18px;
`;

export const OtherLoginBtn = styled.button`
  background: none;
  border: none;
  outline: none;
  height: 45px;
  width:
  margin-left: 13px;
  font-size: 20px;
  font-family: NotoSansKR-M;

  cursor: pointer;

  &:hover {
    background-color: var(--hana-green);
    color: white;
  }
`;
export const LoginLinkContainer = styled.div`
  font-size: 16px;
  background-color: var(--hana-green);
  color: white;

  text-decoration: none;

  display: flex;
  justify-content: center;
  align-items: center;

  width: 430px;
  height: 45px;

  border: solid 1px var(--hana-green);
  border-radius: 18.8px;

  margin-top: 45px;
  margin-bottom: 20px;

  &:hover {
    background-color: white;
    color: var(--hana-green);
  }
`;
export const OriginLoginBtn = styled.button`
  font-size: 20px;
  font-family: NotoSansKR-M;

  color: white;
  background: none;
  border: none;
  outline: none;

  display: flex;
  justify-content: center;
  align-items: center;

  cursor: pointer;

  width: 314px;
  height: px;

  &:hover {
    background-color: white;
    color: var(--hana-green);
    cursor: pointer;
  }
`;
export const WarnId = styled.div`
  font-size: 11px;
  color: var(--greenish-teal);
  margin-left: 140px;
  display: none;
`;
export const WarnPassword = styled.div`
  font-size: 11px;
  color: var(--greenish-teal);
  margin-left: 117px;
  display: none;
`;
export const Row = styled.div`
  display: flex;
  align-items: center;
`;

export const signinDiv = styled.div`
  animation: 1s ${fadeInAnimation};
`;
