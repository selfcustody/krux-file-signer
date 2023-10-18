

class Verify:


    def verify(self):
        """
        onVerify is executed when `verify` command is called

        Args:
            :param parser
                the argument parser instance
        """ 
        verify_file(
            filename=args.verify_file,
            pubkey=args.pub_file,
            sigfile=args.sig_file,
        )
