# Dans settings.py ou un nouveau fichier email_utils.py
from django.core.mail import send_mail
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

def send_delegue_approval_notification(user):
    """
    Envoie un email de notification au délégué après approbation.
    """
    try:
        subject = 'Approbation de votre compte délégué - Université de Yaoundé I'
        message = f"""
Cher/Chère {user.nom},

Nous avons le plaisir de vous informer que votre compte délégué a été approuvé avec succès.

Détails de votre compte :
- Nom : {user.nom}
- Matricule : {user.matricule}
- Email : {user.email}
- Rôle : Délégué

Vous pouvez maintenant vous connecter à l'application avec vos identifiants.

Si vous rencontrez des difficultés pour vous connecter, n'hésitez pas à contacter le support technique.

Cordialement,
L'équipe U-reserve
Université de Yaoundé I
        """
        
        email_sent = send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False
        )
        
        if email_sent:
            logger.info(f"Email d'approbation envoyé avec succès à {user.email}")
            return True
        else:
            logger.error(f"Échec de l'envoi de l'email à {user.email}")
            return False
            
    except Exception as e:
        logger.error(f"Erreur lors de l'envoi de l'email à {user.email}: {str(e)}")
        return False




def send_etudiant_approval_notification(user):
    """
    Envoie un email de notification a l'etudianr après enrégistrement.
    """
    try:
        subject = 'Approbation de votre compte étudiant - Université de Yaoundé I'
        message = f"""
Cher/Chère {user.nom},

Nous avons le plaisir de vous informer que votre compte étudiant a été approuvé avec succès.

Détails de votre compte :
- Nom : {user.nom}
- Matricule : {user.matricule}
- Email : {user.email}
- Rôle : Etudiant

Vous pouvez maintenant vous connecter à l'application avec vos identifiants.

Si vous rencontrez des difficultés pour vous connecter, n'hésitez pas à contacter le support technique.

Cordialement,
L'équipe U-reserve
Université de Yaoundé I
        """
        
        email_sent = send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False
        )
        
        if email_sent:
            logger.info(f"Email d'approbation envoyé avec succès à {user.email}")
            return True
        else:
            logger.error(f"Échec de l'envoi de l'email à {user.email}")
            return False
            
    except Exception as e:
        logger.error(f"Erreur lors de l'envoi de l'email à {user.email}: {str(e)}")
        return False
