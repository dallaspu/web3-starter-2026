<div align="center">

# Web3 in 2026 — where to start

**An annotated link list, for people who think they arrived too late.**

Almost every guide you will find was written in 2020–2022, and a lot of it is now actively wrong: dead testnets, archived tools, URLs that silently redirect somewhere else. **You did not miss the window — you hit a stale guide.**

This page is links. ⛔ None of the projects below are mine. Star counts and last-push dates are the GitHub API's reading on **2026-09-24**; they move, so re-check them before quoting.


</div>

---

## Who this is for

You can already program in something. You have heard the field is "mature now" and that the easy years are gone.

That second half is wrong, and it is wrong in a way that is easy to check. The field is not harder to enter than it was in 2021 — the *documentation* is worse, because most of what ranks is three to five years stale and nobody took it down. Two years ago, following a tutorial meant following a live one. Today the top results mix live and dead together, and nothing on the page tells you which is which.

This list is the filter. It is organised the way the problem actually appears: first the specific things that break, then the shortest path that runs today, then the links.

**What you need to start:** one programming language, and a weekend. Not a maths background, not a blockchain course, not a wallet with money in it.

---

## ⛔ First: if a tutorial says this, it is stale

| A 2022 guide says | In 2026 |
|:--|:--|
| Use Rinkeby / Kovan / Goerli | All gone. Use **Sepolia** (`11155111`) — **Hoodi** (`560048`) is for validator work |
| Use Polygon **Mumbai** | Retired. Use **Amoy** (`80002`) — and its token is **POL**, not MATIC |
| Install **Truffle + Ganache** | **Archived** 2024-04-22. Use **Foundry** — `anvil` replaces Ganache |
| Import **OpenZeppelin 4.x** | Current is **5.x**. `Ownable` takes an owner argument now, and revert strings became custom errors, so old tests stop passing |
| `web3.js` on the frontend | **viem + wagmi** |
| "Account abstraction = ERC-4337" | Now **ERC-4337 + EIP-7702** |
| "The Merge is next" | Five upgrades ago. The one that matters to you is **Dencun** (2024-03) |
| `github.com/ethereum/solidity` | Moved to `argotorg/solidity`. GitHub redirects silently, so the link never errors |
| `book.getfoundry.sh` | Moved to **`getfoundry.sh`** — a `301`, and the paths changed too |

⭐ **The pattern worth carrying: the most-recommended tool and the maintained tool are frequently not the same tool.** Star count measures how long something was popular, not whether it is alive. Check the last-push date before you spend an afternoon on any list, including this one.

---

## Step 0 — Install the environment

Everything below installs in a few minutes on macOS, Linux or WSL.

```bash
curl -L https://foundry.paradigm.xyz | bash
foundryup
forge --version
```

- **[foundry-rs/foundry](https://github.com/foundry-rs/foundry)** ★10,625 · 2026-09-25 — the 2026 default. `forge` builds and tests, `anvil` runs a local chain, `cast` makes one-off calls from the command line.
- **[foundry-rs/forge-std](https://github.com/foundry-rs/forge-std)** ★1,059 · 2026-09-23 — the test standard library. Every Foundry project has it.
- **[remix-project-org/remix-project](https://github.com/remix-project-org/remix-project)** ★3,057 · 2026-09-25 — browser IDE, zero install. **Write your first contract today without installing anything.**
- **[NomicFoundation/hardhat](https://github.com/NomicFoundation/hardhat)** ★8,508 · 2026-09-24 — the TypeScript path, now on **Hardhat 3**, and it ships a Foundry compatibility layer. So this is not either/or — it is Solidity tests vs TypeScript tests.

⛔ **Do not install Truffle or Ganache.** ConsenSys sunset them in September 2023 and the repository was **archived 2024-04-22**, read-only forever. Anything you find that starts with `truffle init` or `ganache-cli` is written for a toolchain that no longer exists — `anvil` does what Ganache did.

**One decision to make here:** tests in Solidity (Foundry) or in TypeScript (Hardhat). Both are current and both are widely used. Foundry is faster and lets you write tests in the same language as the contract; Hardhat is the smoother choice if your team already lives in a JS toolchain.

---

## Step 1 — Learn the language

**Read the language before the frameworks.** Almost every "it doesn't work" question in your first month is a language question wearing a framework costume.

- **[AmazingAng/WTF-Solidity](https://github.com/AmazingAng/WTF-Solidity)** ★14,059 · 2026-08-23 — **Chinese; start here if you read Chinese.** The best-maintained Chinese primer, and it is *current*: its first example is already on `pragma solidity ^0.8.34`.
- **[Solidity docs](https://docs.soliditylang.org/en/latest/)** — the official reference. ⚠️ Skim **[0.8.0 breaking changes](https://docs.soliditylang.org/en/latest/080-breaking-changes.html)** first; twenty minutes, saves a confusing hour.
- **[ethereumbook/ethereumbook](https://github.com/ethereumbook/ethereumbook)** ★21,530 · 2026-09-22 — *Mastering Ethereum*, 2nd ed. manuscript, if you want a book rather than a tutorial.
- **[Cyfrin/foundry-full-course-cu](https://github.com/Cyfrin/foundry-full-course-cu)** ★5,865 · 2026-07-08 — a full Foundry course with code, for learning alongside video.
- **[Cyfrin/Updraft](https://github.com/Cyfrin/Updraft)** ★130 · 2026-07-06 — a free structured curriculum, if you would rather follow a syllabus than assemble one.

⚠️ Old guides say `^0.8.0` or `^0.8.17`; current is **v0.8.37**, but `^0.8.0` still compiles — that part of your tutorial is fine. The version that actually breaks builds is the **library** version, not the compiler version. That is the next section.

---

## The four things that will actually cost you an evening

These are not style preferences. Each one is a case where a 2022 tutorial will take you straight into a wall, and where the error message will not tell you what happened.

**1. OpenZeppelin 4.x imports under a 5.x install.** The single most common way to lose a night. Details below.

**2. A testnet that has been switched off.** You will write correct code, deploy it, and watch it hang — because the network it is aimed at stopped producing blocks years ago. `goerli.etherscan.io` does not resolve today.

**3. A URL that redirects silently.** The repository moved, the tutorial's link still returns `200`, and you land somewhere without being told. `github.com/ethereum/solidity` has been `argotorg/solidity` for a while now.

**4. A tool that was archived in the middle of the tutorial.** Truffle and Ganache are the big two, but the same applies to a long tail of security tools and example repos — see the "archived quietly" table near the end.

⛔ **The rule that covers all four:** if a guide is more than two years old and does not state a version number next to a dependency, verify that dependency before you write code against it.

---

## Step 2 — Three commands

```bash
forge init my-project && cd my-project
forge build && forge test
anvil   # in a second terminal
forge script script/Deploy.s.sol --rpc-url http://localhost:8545 --broadcast
```

`forge init` gives you a working project with a sample contract and a sample test. `anvil` starts a local chain with funded accounts, which is what you deploy against until you have something worth putting on a real testnet.

⚠️ **Pin OpenZeppelin to 5.x.** Release `5.0.0` was deliberately breaking, and it is the change that catches the most people:

- the `Ownable` constructor now takes an owner — `Ownable(msg.sender)`, not `Ownable()`
- `increaseAllowance` / `decreaseAllowance` were **removed**; use `approve` or `forceApprove`
- revert strings became **custom errors** — a test asserting `"Ownable: caller is not the owner"` no longer passes; expect `OwnableUnauthorizedAccount(address)`
- `_beforeTokenTransfer` / `_afterTokenTransfer` were replaced by a single `_update` — a hook override that silently stops being called
- `ERC1155Receiver` was replaced by `ERC1155Holder`

It also raised the minimum compiler to `0.8.20` and moved upgradeable contracts to namespaced storage, so a 4.x → 5.x jump **under a proxy** is unsafe rather than just inconvenient.

---

## Step 3 — Deploy to a real testnet

**Sepolia** (`11155111`). Get test ETH, `forge script --broadcast`, then verify the source on **[sepolia.etherscan.io](https://sepolia.etherscan.io/)**.

⛔ Not Goerli. Not Rinkeby. Not Kovan. Not Ropsten. Not Mumbai. Not Holesky. All six are deprecated or switched off, and a tutorial that names one of them is not wrong about the concept — it is wrong about where to put the code.

**Where the test ETH comes from** is a different problem with its own expiry date. The short version that matters here: the free options mostly gate on **mainnet activity** rather than identity, so a newcomer with an empty mainnet wallet gets the worst queue, and the two best free sources both want you present — one to keep mining, the other to prove you are not a bot. There are whole repositories devoted to tracking which faucets still work; start from **[ethereum.org/en/developers/learning-tools](https://ethereum.org/en/developers/learning-tools/)**.

**What "verify the source" buys you:** anyone can read your contract on the explorer and check that the deployed bytecode matches the code you claim to have written. Do it from your first deployment onward — it costs one command and it is the difference between a contract people can inspect and a black box.

---

## Step 4 — Security — the step 2022 beginners skipped

**2022 taught Solidity as syntax. In 2026 the syntax is the easy part, and the losses are not from syntax errors** — every function you deploy is a public API, and the caller may have read your code more carefully than you did. Reentrancy, ordering, rounding and price manipulation are all legal Solidity; the compiler has nothing to say about them.

In this order:

1. **[OpenZeppelin/ethernaut](https://github.com/OpenZeppelin/ethernaut)** ★2,336 · 2026-09-23 — a browser game, one real vulnerability class per level. **Start here because it is a game:** you will have exploited reentrancy yourself before anyone explains it to you, which is why it sticks.
2. **[SunWeb3Sec/DeFiHackLabs](https://github.com/SunWeb3Sec/DeFiHackLabs)** ★6,797 · 2026-09-25 — real historical exploits as reproducible Foundry tests. This turns knowledge into instinct; reading someone's post-mortem does not.
3. **[crytic/slither](https://github.com/crytic/slither)** ★6,371 · 2026-09-23 — static analyser. Run it on your own contract before you deploy: free, fast, and it catches the boring class of mistake you should never ship.
4. **[crytic/echidna](https://github.com/crytic/echidna)** ★3,181 · 2026-09-23 — property-based fuzzer. You state what must always hold; it tries to break you.
5. **[Cyfrin/aderyn](https://github.com/Cyfrin/aderyn)** ★798 · 2026-09-20 — a second static analyser, written in Rust. Two analysers disagree more often than you would expect, which is the point.

Further in, if this becomes your direction:

- **[Cyfrin/security-and-auditing-full-course-s23](https://github.com/Cyfrin/security-and-auditing-full-course-s23)** ★1,965 · 2026-07-08 — the full auditing curriculum.
- **[Anugrahsr/Awesome-web3-Security](https://github.com/Anugrahsr/Awesome-web3-Security)** ★1,623 · 2026-03-01 — the whole surface in one list.
- **[pcaversaccio/snekmate](https://github.com/pcaversaccio/snekmate)** ★602 · 2026-09-25 — optimised building blocks; advanced, but reading it teaches a lot about what careful code looks like.

**The habit worth forming here:** run the analyser before the deploy, not after. Both of the tools above are free, and neither one is a substitute for thinking — they are for catching the mistakes that are too boring to be interesting.

---

## Step 5 — Your first dApp

- **[scaffold-eth/scaffold-eth-2](https://github.com/scaffold-eth/scaffold-eth-2)** ★2,051 · 2026-08-27 — a complete, forkable full-stack dApp supporting Foundry and Hardhat. **Read it before you write your own.** It answers the questions a tutorial does not: where the contract address lives, how the frontend gets it, what happens when the user is on the wrong network.
- **[wevm/wagmi](https://github.com/wevm/wagmi)** ★6,751 · 2026-09-07 — React hooks for Ethereum; frontend developers start here.
- **[wevm/viem](https://github.com/wevm/viem)** ★3,567 · 2026-09-25 — the TypeScript interface underneath wagmi.
- Python instead? **[ApeWorX/web3.py](https://github.com/ApeWorX/web3.py)** ★5,533 · 2026-08-31 for a library, **[eth-brownie/brownie](https://github.com/eth-brownie/brownie)** ★2,722 · 2026-08-05 for a framework.

---

## Read real code — the fastest way to level up

At some point tutorials stop helping and reading good code is the only thing that moves you. These are large enough to be real and small enough to finish.

- **[Uniswap/v3-core](https://github.com/Uniswap/v3-core)** ★5,024 · 2026-07-30 — the canonical AMM, and still the best-understood one.
- **[Uniswap/v4-core](https://github.com/Uniswap/v4-core)** ★2,534 · 2026-04-24 — read it after v3, to see how a design moves when you are allowed to break it.
- **[ethereum-optimism/optimism](https://github.com/ethereum-optimism/optimism)** ★6,472 · 2026-09-25 — the OP Stack; how an L2 is actually built.
- **[matter-labs/zksync-era](https://github.com/matter-labs/zksync-era)** ★3,236 · 2026-09-24 — how a zk rollup works, from the implementation up.
- **[smartcontractkit/chainlink](https://github.com/smartcontractkit/chainlink)** ★8,249 · 2026-09-25 — oracles, for contracts that need data from outside the chain.
- **[ethereum/go-ethereum](https://github.com/ethereum/go-ethereum)** ★51,369 · 2026-09-24 — the most foundational reference implementation there is. Not a first read; a reference you will come back to.
- **[ethereum/execution-specs](https://github.com/ethereum/execution-specs)** ★1,194 · 2026-09-25 — the execution layer as runnable Python. The definition, not an explanation of the definition.
- **[ethereum/EIPs](https://github.com/ethereum/EIPs)** ★13,988 · 2026-09-24 — why a standard is shaped the way it is. Reading the EIP for something you use is usually faster than reading three articles about it.

---

## Chain data and reference lists

- **[ethereum-lists/chains](https://github.com/ethereum-lists/chains)** ★9,830 · 2026-09-24 — chain metadata registry. **Any chain ID or RPC URL, from the source rather than from memory.** ⚠️ It lists dead networks as `active`, so it is not a liveness check. **[Chainlist](https://chainlist.org/)** is the same data, browsable, for adding a network to a wallet.
- **[bkrem/awesome-solidity](https://github.com/bkrem/awesome-solidity)** ★7,052 · 2026-09-14 — surveying the whole field.
- **[bekatom/awesome-ethereum](https://github.com/bekatom/awesome-ethereum)** ★911 · 2026-08-26 and **[ahmet/awesome-web3](https://github.com/ahmet/awesome-web3)** ★893 · 2026-09-24 — broader sweeps, less curated.

## Archived quietly — still recommended by plenty of lists

Reachable, natural-looking, and no longer current. Every one of these has a healthy star count.

| Old recommendation | Status in 2026 |
|:--|:--|
| `ethereum/solidity-examples` | **Archived** 2023-01-03 |
| `BuidlGuidl/SpeedRunEthereum` | **Archived** 2025-04-23 — use [speedrunethereum.com](https://speedrunethereum.com/) |
| `lambdaclass/cairo-by-example` | **Archived** 2025-05-06 |
| `crytic/awesome-ethereum-security` | ★1,484, no push since 2024-08 |
| `smartcontractkit/full-blockchain-solidity-course-js` | ★14,052, a genuinely good course — but no push since 2024-06, so its toolchain section predates everything in Step 2 |

---

## Official documentation

| Topic | Link |
|:--|:--|
| Ethereum developer hub | [ethereum.org/en/developers/docs](https://ethereum.org/en/developers/docs/) |
| Networks and testnets | [ethereum.org/en/developers/docs/networks](https://ethereum.org/en/developers/docs/networks/) |
| Gas | [ethereum.org/en/developers/docs/gas](https://ethereum.org/en/developers/docs/gas/) |
| Learning tools | [ethereum.org/en/developers/learning-tools](https://ethereum.org/en/developers/learning-tools/) |
| Solidity | [docs.soliditylang.org](https://docs.soliditylang.org/en/latest/) |
| Solidity 0.8 breaking changes | [080-breaking-changes](https://docs.soliditylang.org/en/latest/080-breaking-changes.html) |
| Foundry book | [getfoundry.sh](https://getfoundry.sh/) ⚠️ moved — see the table at the top |
| OpenZeppelin Contracts 5.x | [docs.openzeppelin.com/contracts/5.x](https://docs.openzeppelin.com/contracts/5.x/) |
| Hardhat | [hardhat.org/docs/getting-started](https://hardhat.org/docs/getting-started) |
| viem / wagmi | [viem.sh](https://viem.sh/) · [wagmi.sh](https://wagmi.sh/) |
| EIPs | [eips.ethereum.org](https://eips.ethereum.org/) |
| ERC-4337 | [docs.erc4337.io](https://docs.erc4337.io/) |
| Chainlink | [docs.chain.link](https://docs.chain.link/) |
| Optimism / Arbitrum / Base | [docs.optimism.io](https://docs.optimism.io/) · [docs.arbitrum.io](https://docs.arbitrum.io/) · [docs.base.org](https://docs.base.org/) |
| Sepolia explorer | [sepolia.etherscan.io](https://sepolia.etherscan.io/) |

⚠️ **One correction to link lists you will find elsewhere:** the learning-tools page is at `ethereum.org/en/developers/learning-tools/`. The path with `/docs/` in it — used by several older collections — returns **404**.

---

## If you only take one thing

**The field did not close. The documentation rotted.**

Everything in the first table is a stale link, an archived repository, or a moved URL — none of it is a reason you are late.
